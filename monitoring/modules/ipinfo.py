# System module to collect system info from server
from runners.runner import Runner


async def collect(runner: Runner) -> str:
    command = "hostname -I | awk '{print $1}'"
    result = await runner.run(command)
    return result.rstrip()
