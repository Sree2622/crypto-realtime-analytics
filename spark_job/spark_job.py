import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType, IntegerType

MONGO_URI = "mongodb://mongo:27017"
MONGO_DB = "realtime_db"
MONGO_COLLECTION = "crypto_aggregates"

from pyspark.sql.functions import avg, count


def write_to_mongo(df, epoch_id):
    # Convert DataFrame to Pandas then write to Mongo (small volumes expected in dev)
    records = [row.asDict() for row in df.collect()]
    if not records:
        return
    from pymongo import MongoClient
    client = MongoClient(MONGO_URI)
    coll = client[MONGO_DB][MONGO_COLLECTION]
    for r in records:
        # upsert by window start + symbol
        filter_doc = {"symbol": r["symbol"], "window_start": r["window_start"]}
        update_doc = {"$set": {
            "symbol": r["symbol"],
            "window_start": r["window_start"],
            "window_end": r["window_end"],
            "avg_price": r["avg_price"],
            "count": int(r["cnt"])
        }}
        coll.update_one(filter_doc, update_doc, upsert=True)
    client.close()

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("CryptoStreamProcessor") \
        .getOrCreate()

    # Kafka topic
    kafka_bootstrap = "kafka:9092"

    schema = StructType([
        StructField("symbol", StringType()),
        StructField("price", DoubleType()),
        StructField("ts", LongType())
    ])

    raw = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap) \
        .option("subscribe", "crypto-prices") \
        .option("startingOffsets", "earliest") \
        .load()

    # value is bytes -> string -> json
    df = raw.selectExpr("CAST(value AS STRING) as json_str") \
        .select(from_json(col("json_str"), schema).alias("data")) \
        .select(
            col("data.symbol").alias("symbol"),
            col("data.price").alias("price"),
            to_timestamp((col("data.ts")).cast("timestamp")).alias("event_time")
        )


    agg = df.withWatermark("event_time", "2 minutes") \
        .groupBy(window(col("event_time"), "1 minute"), col("symbol")) \
        .agg(
            avg("price").alias("avg_price"),
            count("*").alias("cnt")   # 👈 add count here
        )

    result = agg.select(
        col("symbol"),
        col("avg_price"),
        col("cnt"),  # 👈 include count
        col("window.start").cast("string").alias("window_start"),
        col("window.end").cast("string").alias("window_end")
    )

    # Write with foreachBatch to MongoDB
    query = result.writeStream \
        .foreachBatch(lambda df, epoch_id: write_to_mongo(df.withColumnRenamed("avg_price", "avg_price").withColumnRenamed("symbol","symbol"), epoch_id)) \
        .outputMode("update") \
        .option("checkpointLocation", "/tmp/spark_checkpoints/crypto") \
        .start()

    query.awaitTermination()

