import os
import json

from dotenv import load_dotenv
from google import genai

# ============================================
# LOAD ENV VARIABLES
# ============================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = os.getenv(
    "GEMINI_MODEL_NAME",
    "gemini-2.0-flash"
)

# ============================================
# INITIALIZE GEMINI CLIENT
# ============================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)

# ============================================
# AI ANALYSIS FUNCTION
# ============================================

def analyze_soc_alert(log_data: dict):

    prompt = f"""
You are the AI reasoning engine for QuadShield Autonomous SOC.

Analyze the following security telemetry.

Determine:
1. Attack Type
2. Severity Score (1-10)
3. Recommended Action
4. Technical Summary

Security Event:
{json.dumps(log_data, indent=2)}

Return ONLY valid JSON using this schema:

{{
    "attack_type": "string",
    "severity": integer,
    "status": "SAFE | INVESTIGATING | BLOCKED",
    "summary": "technical explanation"
}}
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as error:

        print(f"\n[Gemini API Warning] {str(error)}")

        # ============================================
        # FALLBACK MOCK RESPONSE
        # ============================================

        fallback_response = {
            "attack_type": "SSH Brute Force",
            "severity": 8,
            "status": "BLOCKED",
            "summary": (
                "Repeated failed SSH authentication "
                "attempts detected from a suspicious source."
            )
        }

        return fallback_response