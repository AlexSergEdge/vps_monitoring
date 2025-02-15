import asyncio
import importlib
import yaml

from pydantic import ValidationError

from core.config import settings
from ssh.runner import LocalRunner, RemoteRunner
from schemas import Servers


async def run_module(module_name, runner):
    try:
        module = importlib.import_module(f'modules.{module_name}')
        if hasattr(module, 'collect'):
            return await module.collect(runner)
        else:
            print(f"Module '{module_name}' has no 'collect' method.")
    except ModuleNotFoundError:
        print(f"Module '{module_name}' not found.")


async def collect_data():

    result_list = []

    with open(settings.SERVERS_CONFIG, 'r') as servers:
        servers = yaml.safe_load(servers)
    try:
        valid_servers = Servers(**servers)
    except ValidationError as e:
        print(f'Config is invalid! {e}')  # TODO: more info on error
        return

    for server in valid_servers.servers:
        runner = None
        if server.ssh:
            runner = RemoteRunner(
                ip_addr=server.ip,
                port=server.ssh.ssh_port,
                username=server.ssh.ssh_user,
                key=server.ssh.ssh_privkey_path
            )
        else:
            runner = LocalRunner()
        
        result_pool = []
        for module in server.modules:
            collected_data = await run_module(module, runner)
            result_pool.append(collected_data)

        result_list.append(f'Info for {server.name}\n\n{"\n".join(result_pool)}')
    return result_list


if __name__ == '__main__':
    print(asyncio.run(collect_data()))