import os
import json

from dotenv import load_dotenv
from kafka import KafkaConsumer

# ============================================
# LOAD ENVIRONMENT VARIABLES
# ============================================

load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

# ============================================
# CREATE KAFKA CONSUMER
# ============================================

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="quadshield-brain",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("====================================")
print(" QuadShield Kafka Consumer Started ")
print("====================================")

# ============================================
# START LISTENING
# ============================================

for message in consumer:

    event = message.value

    print("\n[+] Incoming Security Event:")
    print(json.dumps(event, indent=4))