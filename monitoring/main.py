import asyncio
import datetime
import importlib
import yaml

from pydantic import ValidationError

from config.config import settings
from runners.runner import LocalRunner, RemoteRunner
from schemas import Servers
from constants.constants import CLOCK_EMOJI


async def run_module(module_name, runner):
    """Run module from ./modules/ with name module_name using specified runner"""
    try:
        # Module must have collect function
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

        timestamp = datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')

        # If we want to get our current machine ip, we can use this hack
        if server.ip in ['localhost', '127.0.0.1']:
            local_server_ip = await run_module('ipinfo', runner)
            server.ip += f' ({local_server_ip})'

        result_list.append(f'{CLOCK_EMOJI} {timestamp}\nHost: <b>{server.name}</b>\nIP: {server.ip}\n\n{"\n".join(result_pool)}')
    return result_list


if __name__ == '__main__':
    print(asyncio.run(collect_data()))