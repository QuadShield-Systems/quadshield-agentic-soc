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

# Point cleanly to your active teammate infrastructure port
KAFKA_BROKER = "localhost:29092"
KAFKA_TOPIC = "soc-alerts"

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
print(" QuadShield Super-Consumer Online    ")
print("====================================")

# ============================================
# START LISTENING
# ============================================

for message in consumer:

    event = message.value

    print("\n[+] Incoming Security Event From Kafka:")
    print(json.dumps(event, indent=4))

    # ============================================
    # 🚨 CORE DATA HYDRO-INTERCEPTOR 🚨
    # Force the root fields inside the event to match what your 
    # team's code structure parses during internal state transitions.
    # ============================================
    raw_log_msg = str(event.get("event", "")).upper()
    kafka_tag = str(event.get("attack_type", "")).upper()

    if "DDOS" in raw_log_msg or "DDOS" in kafka_tag or "SYN_FLOOD" in raw_log_msg:
        print("\n🎯 [INTERCEPT] Forcing core payload schema parameters to DDOS_SYN_FLOOD")
        event["attack_type"] = "DDOS_SYN_FLOOD"
        event["event_type"] = "DDOS_SYN_FLOOD"  # Cover both variants your team's code might read
        event["event"] = "CRITICAL ALERT: DDOS_SYN_FLOOD network anomaly detected on system interfaces"

    elif "SQL" in raw_log_msg or "SQL" in kafka_tag or "UNION" in raw_log_msg:
        print("\n🎯 [INTERCEPT] Forcing core payload schema parameters to SQL_INJECTION")
        event["attack_type"] = "SQL_INJECTION"
        event["event_type"] = "SQL_INJECTION"   # Cover both variants your team's code might read
        event["event"] = "CRITICAL ALERT: SQL_INJECTION malicious web query syntax detected"

    else:
        # 🌟 THE RESTORED THIRD VECTOR CRITICAL FOR BALANCE 🌟
        print("\n🎯 [INTERCEPT] Retaining baseline metrics for SSH_BRUTE_FORCE")
        event["attack_type"] = "SSH_BRUTE_FORCE"
        event["event_type"] = "SSH_BRUTE_FORCE"
        # Keeps your original teammate base log text clean
        if not event.get("event"):
            event["event"] = "Failed password for admin root profile access attempt"

    # ============================================
    # PREPARE LANGGRAPH STATE
    # ============================================

    initial_state = {
        "event": event,
        "ai_result": {},
        "failed_attempts": event.get("failed_attempts", 1),
        "status": "RECEIVED"
    }

    # ============================================
    # EXECUTE LANGGRAPH WORKFLOW
    # ============================================

    try:
        # Pass the modified event context down the workflow path
        result = app.invoke(initial_state)

        print("\n====================================")
        print(" LANGGRAPH WORKFLOW RESULT ")
        print("====================================")
        print(json.dumps(result, indent=4))
        print("\n[+] LangGraph workflow executed successfully.")

    except Exception as e:
        print("\n[-] Error executing LangGraph workflow:")
        traceback.print_exc()