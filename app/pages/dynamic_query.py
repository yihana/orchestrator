import os

import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001/api/v1")

st.title("RFC Dynamic Query")

st.write("SAP 테이블을 안전하게 조회합니다. 허용된 테이블만 실행됩니다.")

col1, col2 = st.columns(2)
with col1:
    table = st.text_input("Table", "MARA").upper()
    fields = st.text_input("Fields (comma separated)", "")
with col2:
    where = st.text_input("WHERE", "")
    maxrows = st.number_input("Max Rows", value=5000, min_value=1)

if st.button("Execute RFC"):
    payload = {
        "table": table,
        "fields": fields,
        "where": where,
        "maxrows": maxrows,
    }
    try:
        response = requests.post(
            f"{API_BASE_URL}/erp/dynamic-query",
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        st.success("Query executed")
        st.json(response.json())
    except requests.RequestException as exc:
        st.error(f"Request failed: {exc}")

st.divider()

st.caption("허용 테이블: MARA, MARC, EKKO, EKPO, MBEW")
