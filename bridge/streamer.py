import os
from dotenv import load_dotenv
from kafka import KafkaProducer
import json

# Load environment variables
load_dotenv()

# Read values from .env
KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Sample SOC alert message
sample_alert = {
    "source": "SOC-Agent",
    "event": "SSH Brute Force Detected",
    "severity": "HIGH"
}

try:
    producer.send(KAFKA_TOPIC, sample_alert)
    producer.flush()

    print(" Alert streamed successfully!")
    print(f" Topic: {KAFKA_TOPIC}")
    print(f" Message: {sample_alert}")

except Exception as e:
    print(" Error while streaming alert:")
    print(e)