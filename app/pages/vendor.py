import json
import os

import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001/api/v1")

st.title("ERP Vendor BAPI")

actions = [
    "GET_OPEN_ITEMS",
    "GET_CURRENT_BALANCE",
    "GET_KEYDATE_BALANCE",
    "GET_VENDOR_DETAIL",
    "FIND_VENDOR",
    "CHECK_VENDOR",
    "CREATE_VENDOR",
    "EDIT_VENDOR",
]

selected_action = st.selectbox("BAPI Action", actions)
params_input = st.text_area("BAPI Parameters (JSON)", "{}", height=200)

if st.button("Execute"):
    try:
        params = json.loads(params_input or "{}")
    except json.JSONDecodeError as exc:
        st.error(f"Invalid JSON: {exc}")
    else:
        try:
            response = requests.post(
                f"{API_BASE_URL}/erp/vendor/execute/{selected_action}",
                json=params,
                timeout=30,
            )
            response.raise_for_status()
            st.success("Execution completed")
            st.json(response.json())
        except requests.RequestException as exc:
            st.error(f"Request failed: {exc}")
