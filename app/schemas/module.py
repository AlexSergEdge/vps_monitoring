from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ModuleBase(BaseModel):
    name: str
    description: str

class Module(ModuleBase):
    id: int
    created_at: datetime

class ModuleCreate(ModuleBase):
    pass