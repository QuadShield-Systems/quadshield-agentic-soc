import os
import json
import time
import random
from datetime import datetime

from dotenv import load_dotenv
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

# ============================================
# LOAD ENVIRONMENT VARIABLES
# ============================================

load_dotenv()
print("KAFKA_BROKER =", os.getenv("KAFKA_BROKER"))
print("KAFKA_TOPIC =", os.getenv("KAFKA_TOPIC"))

KAFKA_BROKER = os.getenv(
    "KAFKA_BROKER",
    "localhost:29092"
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC",
    "soc-alerts"
)

# ============================================
# CREATE KAFKA PRODUCER
# ============================================

try:

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    print("\n====================================")
    print(" QuadShield Mock Generator Started ")
    print("====================================")

except NoBrokersAvailable:

    print("\n[-] Kafka broker is not available.")
    print("[!] Make sure Docker containers are running.")
    exit()
    
# ============================================
# SSH BRUTE FORCE EVENT
# ============================================

def generate_ssh_bruteforce():

    return {
        "timestamp": datetime.now().isoformat(),
        "source_ip": random.choice([
            "185.220.101.5",  # Tor Proxy Node
            "172.16.0.8",     # Rogue Internal Node
            "45.33.22.11"     # Attacker Cloud VPS
        ]),
        "event": "Failed password for admin root profile access attempt",
        "failed_attempts": random.randint(5, 15),
        "severity": "HIGH",
        "attack_type": "SSH_BRUTE_FORCE",
        "status": "DETECTED"
    }

# ============================================
# SQL INJECTION EVENT
# ============================================

def generate_sql_injection():

    return {
        "timestamp": datetime.now().isoformat(),
        "source_ip": random.choice([
            "45.67.12.90",
            "103.21.244.1",
            "192.168.45.12"  # Local Infiltrator Web App Attacker
        ]),
        "event": "UNION SELECT injection attempt on API endpoint auth parameter: id=1' OR '1'='1'--",
        "failed_attempts": random.randint(1, 3),
        "severity": "CRITICAL",
        "attack_type": "SQL_INJECTION",  # Restored pure string
        "status": "DETECTED"
    }
    
# ============================================
# DENIAL OF SERVICE (DDOS) EVENT
# ============================================

def generate_ddos_syn_flood():

    return {
        "timestamp": datetime.now().isoformat(),
        "source_ip": random.choice([
            "88.198.5.2",     # Botnet Controller Node
            "109.201.154.3",  # High-Volume Malicious Spammer
            "203.0.113.55"    # External Stresser Tool Node
        ]),
        "event": "SYN FLOOD Network Anomaly Detected - 7500 packets/sec overwhelming kernel interfaces",
        "failed_attempts": random.randint(100, 500),
        "severity": "CRITICAL",
        "attack_type": "DDOS_SYN_FLOOD",  # Restored pure string
        "status": "DETECTED"
    }

# ============================================
# START STREAMING EVENTS
# ============================================

print("\n[+] Streaming multi-vector mock security logs...\n")
print(f"🎯 Branch: feature/multi-vector-attacks | Pacing: 30 Seconds Delay\n")

while True:

    try:

        # Balance across all three threat profiles seamlessly
        attack_type = random.choice([
            "ssh",
            "sql",
            "ddos"
        ])

        if attack_type == "ssh":
            log = generate_ssh_bruteforce()
        elif attack_type == "sql":
            log = generate_sql_injection()
        else:
            log = generate_ddos_syn_flood()

        # SEND TO KAFKA BROKER CLUSTER
        producer.send(
            KAFKA_TOPIC,
            value=log
        )

        producer.flush()

        print("\n====================================")
        print(f"[🚨 ALERT] Threat Telemetry Ingested into Pipeline")
        print("====================================")

        print(json.dumps(log, indent=4))

        # 30-second presentation pacing loop delay
        time.sleep(30)

    except KeyboardInterrupt:

        print("\n[!] Mock generator stopped manually.")
        break

    except Exception as error:

        print(f"\n[-] Error: {str(error)}")

        time.sleep(30)