import yaml
import json
from bot import send_data
from typing import Optional, List
from pydantic import BaseModel, ValidationError

from core.config import settings


# Config validation
class Server(BaseModel):
    ip: str
    name: str
    ssh: Optional[dict] = None  # TODO: add validations for SSH if exists
    modules: list


class Servers(BaseModel):
    servers: List[Server]


# TODO: here we iterate over config and send aync commands
def collect_data():
    with open(settings.SERVERS_CONFIG, 'r') as servers:
        servers = yaml.safe_load(servers)
    try:
        valid_servers = Servers(**servers)
    except ValidationError as e:
        print('Config is invalid! See example config')
        return

    for server in valid_servers.servers:
        print(server.ip)
        
        if server.ssh:
            print(server.ssh.get('ssh_user', None))

    

collect_data()







# asyncio.run(send_data('Test'))