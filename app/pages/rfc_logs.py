import os

import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001/api/v1")

st.title("RFC Execution Logs")

try:
    response = requests.get(f"{API_BASE_URL}/erp/logs/rfc", timeout=30)
    response.raise_for_status()
    logs = response.json()
except requests.RequestException as exc:
    st.error(f"로그 조회 실패: {exc}")
    logs = []

for log in logs:
    header = f"{log.get('executed_at')} | {log.get('name')}"
    with st.expander(header):
        st.json({
            "params": log.get("params"),
            "result": log.get("result"),
        })
