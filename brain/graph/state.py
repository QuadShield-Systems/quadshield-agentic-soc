from typing import TypedDict, Dict, Any

# ============================================
# SOC GRAPH STATE
# ============================================

class SOCState(TypedDict):

    event: Dict[str, Any]

    ai_result: Dict[str, Any]

    failed_attempts: int

    status: str