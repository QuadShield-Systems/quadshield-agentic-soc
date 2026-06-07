import os
import json
from google import genai  # Adjust this import to match your project's exact Gemini initialization library if different
from langgraph.graph import StateGraph, END

from graph.state import SOCState
from graph.nodes import (
    threshold_node,
    # analyze_node,  # We are swapping this out for our dynamic inline analyzer node
    db_node
)

# ============================================
# NEW DYNAMIC INLINE LLM ANALYZER NODE
# ============================================
def dynamic_analyze_node(state: SOCState):
    """
    Interceptors the LangGraph state and uses Gemini 1.5 Flash to 
    dynamically evaluate if the threat is SSH, SQL Injection, or DDoS.
    """
    event_data = state.get("event", {})
    # Look at the raw string message inside the event
    raw_log_msg = event_data.get("event", "")

    # Clean fallback default structure if the LLM fails
    ai_response = {
        "attack_type": "SSH Brute Force",
        "severity": 7,
        "status": "BLOCKED",
        "summary": "Failed authentication attempt detected."
    }

    # Construct a high-performance dynamic prompt for Gemini 1.5 Flash
    system_prompt = f"""
    You are an expert Agentic SOC Security Automation Analyst.
    Analyze this raw security event text log message carefully:
    "{raw_log_msg}"

    CRITICAL ANALYSIS INSTRUCTIONS:
    1. Read the wording inside the text string.
    2. If the text mentions 'SQL_INJECTION' or 'UNION SELECT', classify 'attack_type' as 'SQL_INJECTION', set severity to 9, and status to 'FILTERED'.
    3. If the text mentions 'DDOS_SYN_FLOOD' or 'packets/sec', classify 'attack_type' as 'DDOS_SYN_FLOOD', set severity to 10, and status to 'MITIGATED'.
    4. If it is regular authentication text, classify 'attack_type' as 'SSH_BRUTE_FORCE', set severity to 7, and status to 'BLOCKED'.

    You must respond STRICTLY with a valid, clean JSON block matching this exact structure:
    {{
        "attack_type": "THE_CLASSIFIED_TYPE_STRING",
        "severity": integer_value_1_to_10,
        "status": "STATUS_STRING",
        "summary": "A precise, automated context summary of the raw exploit telemetry"
    }}
    """

    try:
        # Initialize Gemini client using your environment API key variables
        # Note: If your project uses standard 'google-generativeai', swap this client call to match your nodes pattern
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=system_prompt,
            config={'response_mime_type': 'application/json'}
        )
        
        # Parse clean semantic JSON result out of the model response stream
        ai_response = json.loads(response.text.strip())
        
    except Exception as e:
        print(f"\n[-] Gemini Parsing Exception encountered: {str(e)}")
        # If API errors out, let's look at the string manually to guarantee a backup update happens
        if "SQL_INJECTION" in raw_log_msg:
            ai_response = {
                "attack_type": "SQL_INJECTION",
                "severity": 9,
                "status": "FILTERED",
                "summary": "Rule-based backup interceptor: SQL Injection threat string detected."
            }
        elif "DDOS" in raw_log_msg:
            ai_response = {
                "attack_type": "DDOS_SYN_FLOOD",
                "severity": 10,
                "status": "MITIGATED",
                "summary": "Rule-based backup interceptor: Distributed Denial of Service anomaly detected."
            }

    # Update the LangGraph workflow dictionary state variables
    state["ai_result"] = ai_response
    state["status"] = "ANALYZED"
    return state

# ============================================
# BUILD WORKFLOW
# ============================================

workflow = StateGraph(SOCState)

# ============================================
# ADD NODES
# ============================================

workflow.add_node(
    "threshold_node",
    threshold_node
)

# Crucial Fix: Swapping your team's fixed node for our new dynamic AI interpreter node
workflow.add_node(
    "analyze_node",
    dynamic_analyze_node
)

workflow.add_node(
    "db_node",
    db_node
)

# ============================================
# ENTRY POINT
# ============================================

workflow.set_entry_point(
    "threshold_node"
)

# ============================================
# FLOW EDGES
# ============================================

workflow.add_edge(
    "threshold_node",
    "analyze_node"
)

workflow.add_edge(
    "analyze_node",
    "db_node"
)

workflow.add_edge(
    "db_node",
    END
)

# ============================================
# COMPILE WORKFLOW APPLICATION
# ============================================

app = workflow.compile()