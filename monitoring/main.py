import asyncio
import yaml

from bot import send_data

from pydantic import ValidationError

from core.config import settings
from ssh.runner import LocalRunner, RemoteRunner
from schemas import Servers


async def collect_data():
    with open(settings.SERVERS_CONFIG, 'r') as servers:
        servers = yaml.safe_load(servers)
    try:
        valid_servers = Servers(**servers)
    except ValidationError as e:
        print(f'Config is invalid! {e}')  # TODO: more info on error
        return

    for server in valid_servers.servers:
        print(server.ip)
        
        if server.ssh:
            print(server.ssh.ssh_user)


asyncio.run(collect_data())


# asyncio.run(send_data('Test'))