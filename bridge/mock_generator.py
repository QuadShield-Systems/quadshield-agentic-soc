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
    "localhost:9092"
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
            "192.168.1.105",
            "10.0.0.23",
            "172.16.0.8"
        ]),

        "event": "Failed password for admin",

        "failed_attempts": random.randint(5, 15),

        "severity": "HIGH",

        "attack_type": "SSH_BRUTE_FORCE"
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
            "185.220.101.5"
        ]),

        "event": "UNION SELECT attack detected",

        "failed_attempts": random.randint(1, 3),

        "severity": "CRITICAL",

        "attack_type": "SQL_INJECTION"
    }
    
# ============================================
# START STREAMING EVENTS
# ============================================

print("\n[+] Streaming mock security logs...\n")

while True:

    try:

        attack_type = random.choice([
            "ssh",
            "sql"
        ])

        if attack_type == "ssh":

            log = generate_ssh_bruteforce()

        else:

            log = generate_sql_injection()

        # SEND TO KAFKA
        producer.send(
            KAFKA_TOPIC,
            value=log
        )

        producer.flush()

        print("\n====================================")
        print("[+] Event Sent To Kafka")
        print("====================================")

        print(json.dumps(log, indent=4))

        # WAIT BEFORE NEXT EVENT
        time.sleep(3)

    except KeyboardInterrupt:

        print("\n[!] Mock generator stopped manually.")
        break

    except Exception as error:

        print(f"\n[-] Error: {str(error)}")

        time.sleep(5)