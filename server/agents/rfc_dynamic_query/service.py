from server.agents.erp_adapter import ERPAdapter
from server.db.erp_crud import log_rfc_execution
from .validator import validate_query


class RFCDynamicQueryAgent:
    def __init__(self):
        self.adapter = ERPAdapter()

    def execute(self, req):
        validate_query(req)

        result = self.adapter.call_rfc(
            rfc_name="Z_RFC_DYNAMIC_QUERY",
            params={
                "IV_TABLE": req.table.upper(),
                "IV_FIELDS": req.fields or "",
                "IV_WHERE": req.where or "",
                "IV_MAXROWS": req.maxrows,
            },
        )

        log_rfc_execution(
            rfc_name="Z_RFC_DYNAMIC_QUERY",
            params=req.model_dump(),
            result=result,
        )

        return result
