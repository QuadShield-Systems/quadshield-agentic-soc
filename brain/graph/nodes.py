from utils.gemini_client import analyze_soc_alert
from utils.db import insert_security_result

# ============================================
# THRESHOLD NODE
# ============================================

def threshold_node(state):

    print("\n[+] Checking Attack Threshold...\n")

    attempts = state["failed_attempts"]

    if attempts >= 5:

        state["status"] = "INVESTIGATING"

    else:

        state["status"] = "SAFE"

    return state

# ============================================
# ANALYSIS NODE
# ============================================

def analyze_node(state):

    print("\n[+] Running AI Analysis Node...\n")

    event = state["event"]

    result = analyze_soc_alert(event)

    state["ai_result"] = result

    state["status"] = "ANALYZED"

    return state

# ============================================
# DATABASE NODE
# ============================================

def db_node(state):

    print("\n[+] Writing Result To Supabase...\n")

    db_payload = {

        "source_ip": "172.20.0.3",

        "event_type": "SSH_BRUTE_FORCE",

        "status": state["ai_result"]["status"],

        "severity": state["ai_result"]["severity"],

        "raw_log_data": str(state["ai_result"])
    }

    insert_security_result(db_payload)

    return state