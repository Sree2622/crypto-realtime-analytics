# Real-Time Cryptocurrency Analytics Platform

A full-stack real-time data pipeline for live cryptocurrency analytics.  
Ingests live crypto prices, processes them with Spark, stores results in MongoDB, and visualizes on a React dashboard.

---

## Features
- Live data ingestion from CoinGecko API  
- Real-time streaming with Kafka + Spark Structured Streaming  
- Aggregated crypto price storage in MongoDB  
- REST API built with Flask  
- Interactive React dashboard with live BTC & ETH charts  
- Containerized with Docker Compose  

---

## Tech Stack
- Backend: Kafka, Spark, Flask, MongoDB  
- Frontend: React (Vite)  
- Containerization: Docker & Docker Compose  
- Data Source: CoinGecko API  

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/crypto-realtime-analytics.git
cd crypto-realtime-analytics
```

### 2. Start backend services
```bash
sudo docker compose up --build -d
```

### 3. Start the frontend dashboard
```bash
sudo docker compose up --build -d
```

