from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class VpsBase(BaseModel):
    hostname: str
    ip_address: str
    country: str

class Vps(VpsBase):
    id: int
    created_at: datetime

class VpsCreate(VpsBase):
    ssh_port: Optional[int]
    ssh_user: Optional[str]
    ssh_public_key_path: Optional[str]