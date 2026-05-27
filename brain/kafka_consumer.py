import os
import json
import traceback

from dotenv import load_dotenv
from kafka import KafkaConsumer

# LangGraph Workflow Import
from graph.workflow import app

# ============================================
# LOAD ENVIRONMENT VARIABLES
# ============================================

load_dotenv()

KAFKA_BROKER = os.getenv(
    "KAFKA_BROKER",
    "localhost:9092"
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC",
    "soc-alerts"
)

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

    # ============================================
    # PREPARE LANGGRAPH STATE
    # ============================================

    initial_state = {
        "event": event,
        "ai_result": {},
        "failed_attempts": event.get(
            "failed_attempts",
            1
        ),
        "status": "RECEIVED"
    }

    # ============================================
    # EXECUTE LANGGRAPH WORKFLOW
    # ============================================

    try:

        result = app.invoke(initial_state)

        print("\n====================================")
        print(" LANGGRAPH WORKFLOW RESULT ")
        print("====================================")

        print(json.dumps(result, indent=4))

        print("\n[+] LangGraph workflow executed successfully.")

    except Exception as e:

        print("\n[-] Error executing LangGraph workflow:")

        traceback.print_exc()