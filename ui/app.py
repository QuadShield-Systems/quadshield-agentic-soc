import streamlit as st
import os
from dotenv import load_dotenv

# Load system configurations from the brain or root if available
load_dotenv()

# 1. Page Configuration Framework Setup
st.set_page_config(
    page_title="QuadShield Autonomous SOC",
    page_icon="🛡️",
    layout="wide"
)

# 2. Strategic Dashboard Header Banner
st.title("🛡️ QuadShield Systems — Autonomous SOC Dashboard")
st.markdown("### Real-Time Threat Analysis & Agentic Incident Response Pipelines")
st.markdown("---")

# 3. Dynamic KPI Metrics Row
metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric(
        label="Log Highway Ingestion (Kafka)", 
        value="CONNECTED", 
        delta="Port 9092 Routing Live",
        delta_color="normal"
    )

with metric_col2:
    st.metric(
        label="Autonomous Reasoner (Gemini AI)", 
        value="ACTIVE", 
        delta="LangGraph Engine Ready",
        delta_color="normal"
    )

with metric_col3:
    st.metric(
        label="Central Database Sync (Supabase)", 
        value="STABLE", 
        delta="Schema Up To Date",
        delta_color="normal"
    )

st.markdown("### 🚨 Latest Security Operations Telemetry Logs")

# 4. Monitored Event Threat Containment Card
with st.container(border=True):
    st.subheader("Current Active Threat Vector Analysis")
    
    # Internal horizontal metric alignments
    status_col, severity_col, source_col = st.columns([1, 1, 2])
    with status_col:
        st.warning("⚠️ INVESTIGATING")
    with severity_col:
        st.error("SEVERITY: 8/10")
    with source_col:
        st.code("Target: Host-Ubuntu-Victim-Node")
        
    # Read-only stream visualization displaying raw mock data structure
    st.text_area(
        label="Intercepted Network Event String:",
        value="May 28 18:47:12 ubuntu sshd[4092]: Failed password for invalid user admin from 192.168.1.105 port 43210 ssh2",
        height=68,
        disabled=True
    )
    
    # Brain Reasoning Output Board
    st.markdown("#### 🧠 AI Decision Matrix & Recommended Remediation Actions")
    st.info(
        "**Threat Profile Evaluation:** Massive cluster of authentication failures hitting administrative root parameters. "
        "Pattern cleanly establishes a malicious automated **SSH Brute-Force Attack** profile targeting enterprise infrastructure.\n\n"
        "**Mitigation Execution Plan:** Border firewall tracking commands issued automatically to drop packets originating from source IP `192.168.1.105`. "
        "Recommended protocol adjustment tracking: transition user entry rules strictly to SSH Key authentication schemes."
    )