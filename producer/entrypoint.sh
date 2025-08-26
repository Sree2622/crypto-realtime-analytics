#!/bin/bash
echo "Waiting 10 seconds for Kafka to be ready..."
sleep 10
exec python -u producer.py

