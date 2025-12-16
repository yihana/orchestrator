import json

from fastapi import APIRouter, HTTPException

from server.agents.bapi.vendor_agent import VendorAgent
from server.agents.rfc_dynamic_query.schema import DynamicQueryRequest
from server.agents.rfc_dynamic_query.service import RFCDynamicQueryAgent
from server.db.erp_crud import get_bapi_logs, get_rfc_logs

router = APIRouter(prefix="/api/v1/erp", tags=["erp"])

vendor_agent = VendorAgent()
dynamic_query_agent = RFCDynamicQueryAgent()


def _serialize_log(log):
    payload = log.params
    result = log.result
    try:
        payload = json.loads(payload)
    except Exception:
        pass
    try:
        result = json.loads(result)
    except Exception:
        pass
    return {
        "id": log.id,
        "name": getattr(log, "bapi_name", None) or getattr(log, "rfc_name", None),
        "params": payload,
        "result": result,
        "executed_at": log.executed_at,
    }


@router.post("/vendor/execute/{action}")
def execute_vendor_bapi(action: str, params: dict):
    try:
        return vendor_agent.execute(action, params)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Vendor BAPI execution failed: {exc}")


@router.get("/logs/bapi")
def list_bapi_logs(limit: int = 100):
    logs = get_bapi_logs(limit)
    return [_serialize_log(log) for log in logs]


@router.post("/dynamic-query")
def dynamic_query(req: DynamicQueryRequest):
    try:
        return dynamic_query_agent.execute(req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Dynamic query failed: {exc}")


@router.get("/logs/rfc")
def list_rfc_logs(limit: int = 100):
    logs = get_rfc_logs(limit)
    return [_serialize_log(log) for log in logs]
