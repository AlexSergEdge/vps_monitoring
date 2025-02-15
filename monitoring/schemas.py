from typing import Optional, List
from pydantic import BaseModel


# Schemas to validate config file

# TODO: create @validators
class SshConnInfo(BaseModel):
    ssh_port: int
    ssh_user: str
    ssh_privkey_path: str


class Server(BaseModel):
    ip: str
    name: str
    ssh: Optional[SshConnInfo] = None
    modules: list


class Servers(BaseModel):
    servers: List[Server]