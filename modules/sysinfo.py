# System module to collect system info from server
from runners.runner import Runner

CPU_MEM_EMOJI = '\U0001F4BB'
SMALL_WHITE_SQUARE_POINT = '\U000025AB'

async def collect(runner: Runner) -> str:

    command = 'top -b -n 1 | grep "%Cpu(s)\\|MiB Mem"'
    result = await runner.run(command)
    # Output:
    # %Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
    # MiB Mem :   1971.3 total,    235.0 free,   1208.6 used,    527.6 buff/cache

    result = "\n".join([f'{SMALL_WHITE_SQUARE_POINT} {res}' for res in result.split('\n') if res])

    message = f"- <b>CPU and memory info {CPU_MEM_EMOJI}:</b>\n{result}\n"
    return message
