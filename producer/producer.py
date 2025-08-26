import time
import json
import requests
from kafka import KafkaProducer

# Kafka broker info
host = "kafka"
port = 9092
TOPIC = "crypto-prices"

# Producer setup
producer = KafkaProducer(
    bootstrap_servers=f"{host}:{port}",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    linger_ms=10,
)

def fetch_prices():
    """Fetch BTC & ETH prices from CoinGecko API"""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd",
        "include_last_updated_at": "true"
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

def produce_loop(interval=10):
    """Produce price updates to Kafka topic"""
    while True:
        try:
            data = fetch_prices()
            ts = int(time.time())
            for coin, payload in data.items():
                msg = {
                    "symbol": coin,
                    "price": payload.get("usd"),
                    "ts": payload.get("last_updated_at", ts),
                }
                producer.send(TOPIC, value=msg)
                print("Produced:", msg)
            producer.flush()
        except Exception as e:
            print("Producer error:", e)
        time.sleep(interval)

if __name__ == "__main__":
    produce_loop(10)

