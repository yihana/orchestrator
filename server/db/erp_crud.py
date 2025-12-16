import json
from typing import List

from sqlalchemy.orm import Session

from server.db.database import SessionLocal
from server.db.erp_models import BAPIExecutionLog, RFCExecutionLog


def log_bapi_execution(bapi_name: str, params: dict, result: dict):
    db: Session = SessionLocal()
    try:
        log = BAPIExecutionLog(
            bapi_name=bapi_name,
            params=json.dumps(params, ensure_ascii=False),
            result=json.dumps(result, ensure_ascii=False),
        )
        db.add(log)
        db.commit()
    finally:
        db.close()


def get_bapi_logs(limit: int = 100) -> List[BAPIExecutionLog]:
    db: Session = SessionLocal()
    try:
        return (
            db.query(BAPIExecutionLog)
            .order_by(BAPIExecutionLog.executed_at.desc())
            .limit(limit)
            .all()
        )
    finally:
        db.close()


def log_rfc_execution(rfc_name: str, params: dict, result: dict):
    db: Session = SessionLocal()
    try:
        log = RFCExecutionLog(
            rfc_name=rfc_name,
            params=json.dumps(params, ensure_ascii=False),
            result=json.dumps(result, ensure_ascii=False),
        )
        db.add(log)
        db.commit()
    finally:
        db.close()


def get_rfc_logs(limit: int = 100) -> List[RFCExecutionLog]:
    db: Session = SessionLocal()
    try:
        return (
            db.query(RFCExecutionLog)
            .order_by(RFCExecutionLog.executed_at.desc())
            .limit(limit)
            .all()
        )
    finally:
        db.close()
