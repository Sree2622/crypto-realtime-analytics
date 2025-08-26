Real-Time Cryptocurrency Analytics Platform

A full-stack real-time data pipeline that ingests live cryptocurrency prices, processes them with Spark Streaming, stores results in MongoDB, and visualizes trends on a React dashboard.

Features

Live data ingestion from CoinGecko API

Real-time streaming using Apache Kafka + Spark Structured Streaming.

Aggregated crypto price storage in MongoDB.

REST API built with Flask to serve aggregated data.

Interactive React dashboard with live charts (Bitcoin & Ethereum).

Fully containerized with Docker Compose.



Getting Started
1 Clone the repo

2 Start backend services (Kafka, Spark, Flask API, MongoDB, Producer)
    sudo docker compose up --build -d

3 Start the frontend dashboard
    cd frontend
    npm install
    npm start

