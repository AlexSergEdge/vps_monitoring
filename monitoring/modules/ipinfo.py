# System module to collect system info from server
from ssh.runner import Runner


async def collect(runner: Runner):
    command = "hostname -I | awk '{print $1}'"
    result = await runner.run(command)
    return result.rstrip()
