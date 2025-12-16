import json

from server.agents.erp_adapter import ERPAdapter
from server.db.erp_crud import log_bapi_execution
from .bapi_map import BAPI_MAP


class VendorAgent:
    def __init__(self):
        self.adapter = ERPAdapter()

    def execute(self, action: str, params: dict):
        normalized_action = action.upper()
        if normalized_action not in BAPI_MAP:
            raise KeyError(f"Unsupported BAPI action: {action}")

        bapi_name = BAPI_MAP[normalized_action]
        result = self.adapter.call_bapi(bapi_name, params)

        log_bapi_execution(
            bapi_name=bapi_name,
            params=params,
            result=result,
        )

        return json.loads(json.dumps(result, ensure_ascii=False))
