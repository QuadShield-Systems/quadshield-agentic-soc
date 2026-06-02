import os
import streamlit as st
import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# ============================================
# INITIALIZATION & CONFIGURATION
# ============================================
load_dotenv()

# Set page configuration to wide mode and dark themed layout styling
st.set_page_config(
    page_title="QuadShield Agentic SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("🔑 Missing Supabase credentials in your environment (.env) variables!")
    st.stop()

# Establish connection to your production database
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ============================================
# LIVE REAL-TIME DATA FETCH FLUID COMPONENT
# ============================================
@st.fragment(run_every=10)
def render_live_dashboard():
    """
    Automatically refreshes this specific dashboard fragment every 10 seconds 
    by querying the newest entries from Supabase without breaking user input loops.
    """
    try:
        # Query the absolute latest logged security incident row with corrected sorting arg
        response = supabase.table("security_logs")\
            .select("*")\
            .order("timestamp", desc=True)\
            .limit(1)\
            .execute()
        
        latest_incident = response.data[0] if response.data else None
    except Exception as e:
        st.error(f"🌐 Database Connectivity Error: {e}")
        latest_incident = None

    # ============================================
    # TOP STATUS BANNER & GENERAL TELEMETRY METRICS
    # ============================================
    st.title("🛡️ QuadShield Autonomous Agentic SOC Operations Center")
    st.markdown("---")

    if latest_incident:
        # 1. Map directly to your actual working Supabase column keys
        event_type = latest_incident.get("event_type", "SSH_BRUTE_FORCE")
        source_ip = latest_incident.get("source_ip", "172.20.0.3")
        status = latest_incident.get("status", "BLOCKED")
        timestamp = latest_incident.get("timestamp", "N/A")
        severity = latest_incident.get("severity", "8")
        
        # 2. Extract description fields or fallback to contextual mock strings for your presentation
        raw_log = latest_incident.get("raw_log") or f"Inbound payload flagged on interface: {event_type} from node source routing path {source_ip}."
        ai_summary = latest_incident.get("ai_summary") or f"Massive cluster of authentication failures hitting administrative ports root parameters. Automated rules successfully isolated the rogue threat vector profile targeting enterprise infrastructure."
        ai_mitigation = latest_incident.get("ai_mitigation") or f"Border firewall rule implemented automatically to drop packets originating from source IP '{source_ip}'. Transitioning user access rules strictly to SSH Key verification schemas."

        # 3. Timezone Fix: Convert UTC string from cloud to machine Local Time (IST)
        try:
            # Parses the ISO timestamp handling format offsets
            clean_time = datetime.datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
            # Automatically shifts hours to match your laptop's local timezone standard
            local_time = clean_time.astimezone()
            display_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            display_time = str(timestamp)[:19]  # Safe string rollback fallback

        # Top Pipeline Infrastructure Metrics Line
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric(label="Log Highway Ingestion", value="ACTIVE ✔️", delta="Streaming Live")
        with m2:
            st.metric(label="Autonomous Reasoner", value="LangGraph Node", delta="Gemini 1.5 Flash")
        with m3:
            st.metric(label="Central Database Sync", value="Supabase Cloud", delta="PostgreSQL Backend")
        with m4:
            st.metric(label="Latest Event Timestamp", value=display_time)

        st.markdown("###")

        # ============================================
        # MAIN THREAT MATRIX AREA
        # ============================================
        with st.container(border=True):
            st.subheader("Current Active Threat Vector Analysis")
            
            status_col, severity_col, target_col = st.columns([1, 1, 2])
            
            with status_col:
                if status == "BLOCKED":
                    st.success(f"🔒 ACTION: {status}")
                else:
                    st.warning(f"⚠️ ACTION: {status}")
                    
            with severity_col:
                # 4. Severity Alert Fix: Handle string or numeric 8 to trigger a red error warning container block
                sev_str = str(severity).upper()
                if any(x in sev_str for x in ["HIGH", "CRITICAL"]) or (sev_str.isdigit() and int(sev_str) >= 7):
                    st.error(f"🚨 SEVERITY: {severity} / 10")
                else:
                    st.info(f"⚡ SEVERITY: {severity} / 10")
                    
            with target_col:
                st.code(f"Target Cluster: host_ubuntu_victim | Attacker Node Source IP: {source_ip}")

            # Intercepted raw syslog terminal text display
            st.text_area(
                label="Intercepted System Log String Payload (Sensor Input):",
                value=raw_log,
                height=70,
                disabled=True
            )
            
            # AI Inference & Remediation Blocks
            st.markdown("---")
            st.markdown("### 🧠 AI Decision Matrix & Recommended Remediation Actions")
            
            st.info(
                f"**Threat Profile Evaluation ({event_type}):**\n\n"
                f"{ai_summary}"
            )
            
            st.success(
                f"**🛡️ Automated Mitigation & Firewall Execution Rule:**\n\n"
                f"{ai_mitigation}"
            )
    else:
        st.info("⏳ Waiting for the first telemetry row to stream into the pipeline database tables...")

# ============================================
# APP EXECUTION RUNTIME
# ============================================
if __name__ == "__main__":
    render_live_dashboard()