from typing import Optional

from pydantic import BaseModel


class DynamicQueryRequest(BaseModel):
    table: str
    fields: Optional[str] = ""
    where: Optional[str] = ""
    maxrows: int = 5000
