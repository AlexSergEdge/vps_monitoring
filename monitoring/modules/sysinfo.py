# System module to collect system info from server
from ssh.runner import Runner


async def collect(runner: Runner):

    command = 'top -b -n 1 | grep "%Cpu(s)\\|MiB Mem"'
    result = await runner.run(command)
    # Output:
    # %Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
    # MiB Mem :   1971.3 total,    235.0 free,   1208.6 used,    527.6 buff/cache

    message = f"- CPU and memory info:\n{result}"
    return message
