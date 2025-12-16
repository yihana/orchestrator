from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from server.db.database import Base


class BAPIExecutionLog(Base):
    __tablename__ = "bapi_execution_logs"

    id = Column(Integer, primary_key=True)
    bapi_name = Column(String, nullable=False)
    params = Column(Text, nullable=False)
    result = Column(Text, nullable=False)
    executed_at = Column(DateTime, default=datetime.utcnow)


class RFCExecutionLog(Base):
    __tablename__ = "rfc_execution_logs"

    id = Column(Integer, primary_key=True)
    rfc_name = Column(String, nullable=False)
    params = Column(Text, nullable=False)
    result = Column(Text, nullable=False)
    executed_at = Column(DateTime, default=datetime.utcnow)
