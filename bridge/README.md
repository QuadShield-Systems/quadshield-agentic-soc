# Bridge Layer - Agentic SOC

## Overview

The Bridge Layer is responsible for real-time event streaming within the Agentic SOC architecture.

This module streams SOC alerts and security events into Apache Kafka topics, enabling communication between:
- Detection Systems
- AI Brain / LangGraph Agents
- Database Layer
- Dashboard / UI

---

## Current Functionality

Implemented:
- Kafka Producer
- Dockerized Kafka Infrastructure
- Environment Variable Configuration
- Real-time SOC Alert Streaming

Current Kafka Topic:
```text
soc-alerts
```

Sample Event Payload:
```json
{
  "source": "SOC-Agent",
  "event": "SSH Brute Force Detected",
  "severity": "HIGH"
}
```

---

## Project Structure

```text
bridge/
│
├── streamer.py
├── requirements.txt
├── README.md
├── .env
└── test_logs/
```

---

## Requirements

- Python 3.10+
- Docker Desktop
- Kafka (via Docker Compose)

---

## Python Dependencies

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create `.env` inside the `bridge/` folder:

```env
KAFKA_BROKER=localhost:9092
KAFKA_TOPIC=soc-alerts
```

---

## Kafka Infrastructure Setup

Kafka and Zookeeper are managed using Docker Compose.

From the root project folder:

```bash
docker compose up -d
```

Verify containers:

```bash
docker ps
```

Expected containers:
- kafka
- zookeeper

---

## Running the Streamer

Navigate into the bridge folder:

```bash
cd bridge
```

Activate virtual environment (Windows PowerShell):

```bash
.\venv\Scripts\Activate
```

Run the Kafka producer:

```bash
python streamer.py
```

Expected output:

```text
Alert streamed successfully!
Topic: soc-alerts
```

---

## Architecture Flow

```text
SOC Detection
      ↓
Bridge Layer (Kafka Producer)
      ↓
Kafka Topic (soc-alerts)
      ↓
AI Brain / Consumers
      ↓
Database / Dashboard
```

---

## Future Enhancements

Planned:
- Kafka Consumers
- Database Integration (PostgreSQL/Supabase)
- Multi-topic Routing
- Alert Prioritization
- Stream Analytics
- AI-driven Event Processing

---

## Notes

Do NOT commit:
- `.env`
- `venv/`
- `__pycache__/`

These are ignored through `.gitignore`.
```cd