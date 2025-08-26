from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017")
DB_NAME = "realtime_db"
COLLECTION = "crypto_aggregates"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
coll = db[COLLECTION]

@app.route("/aggregates")
def aggregates():
    # optional ?symbol=bitcoin
    symbol = request.args.get("symbol")
    q = {}
    if symbol:
        q["symbol"] = symbol
    docs = list(coll.find(q, {"_id": 0}).sort([("window_start", -1)]).limit(50))
    return jsonify(docs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

