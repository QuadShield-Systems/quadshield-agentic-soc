from graph.workflow import app

# ============================================
# MOCK SECURITY EVENT
# ============================================

mock_event = {
    "source": "SOC-Agent",
    "event": "SSH Brute Force Detected",
    "severity": "HIGH"
}

# ============================================
# INITIAL STATE
# ============================================

initial_state = {
    "event": mock_event,
    "ai_result": {},
    "failed_attempts": 12,
    "status": "RECEIVED"
}

# ============================================
# EXECUTE WORKFLOW
# ============================================

result = app.invoke(initial_state)

# ============================================
# PRINT RESULT
# ============================================

print("\n====================================")
print(" FINAL SOC STATE ")
print("====================================\n")

print(result)