from langgraph.graph import StateGraph, END

from graph.state import SOCState

from graph.nodes import (
    threshold_node,
    analyze_node,
    db_node
)

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

workflow.add_node(
    "analyze_node",
    analyze_node
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
# FLOW
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
# COMPILE
# ============================================

app = workflow.compile()