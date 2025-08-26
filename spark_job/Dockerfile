# Use Bitnami Spark image (with Hadoop + Java preconfigured)
FROM bitnami/spark:3.4.1

# Switch to root to install Python + pip
USER root

# Install Python3 and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    rm -rf /var/lib/apt/lists/*


# Download Spark Kafka connector JARs (matching Spark 3.4.1, Scala 2.12)
RUN curl -L -o /opt/bitnami/spark/jars/spark-sql-kafka-0-10_2.12-3.4.1.jar \
      https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.4.1/spark-sql-kafka-0-10_2.12-3.4.1.jar \
 && curl -L -o /opt/bitnami/spark/jars/spark-token-provider-kafka-0-10_2.12-3.4.1.jar \
      https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.4.1/spark-token-provider-kafka-0-10_2.12-3.4.1.jar \
 && curl -L -o /opt/bitnami/spark/jars/kafka-clients-3.5.1.jar \
      https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.5.1/kafka-clients-3.5.1.jar \
 && curl -L -o /opt/bitnami/spark/jars/commons-pool2-2.11.1.jar \
      https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar


# Set workdir
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy Spark job code
COPY spark_job.py .

# Run Spark job
CMD ["spark-submit", "--master", "local[*]", "spark_job.py"]

