from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class HistoryBase(BaseModel):
    vps_id: int
    status: str
    data: str

class History(HistoryBase):
    id: int
    created_at: datetime

class HistoryCreate(HistoryBase):
    pass