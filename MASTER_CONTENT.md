# QuadShield: Master Context (v1.0)

## 🎯 Project Goal
Autonomous mitigation of SSH Brute Force attacks using Agentic AI within a 20-day sprint.

## 👥 The QuadShield Team
- **Member 1 (Lab):** Infrastructure, Docker, Kali/Ubuntu.
- **Member 2 (Bridge):** FastAPI, Log Streaming, Supabase.
- **Member 3 (Logic):** LangGraph, Gemini AI Reasoning.
- **Member 4 (Lead/UI):** Project Integration, Streamlit Dashboard.

## 🗄️ Database Schema (Supabase)
**Table Name:** `security_logs`
- **Columns:** `id`, `timestamp`, `source_ip`, `event_type`, `severity`, `status`, `raw_log_data`

## 🚀 Constraints & Security Architecture
- **Database Security:** Row Level Security (RLS) is **ENABLED**.
- **Database Policies:** Public `INSERT` and public `SELECT` policies are active via the `anon` key.
- **AI Engine:** Use strictly Gemini 1.5 Flash for reasoning.
- **AI Chat Strategy:** Clean-Slate AI policy (Reset chats if logic diverges).
- **Repository Folder:** `quadshield-agentic-soc`
