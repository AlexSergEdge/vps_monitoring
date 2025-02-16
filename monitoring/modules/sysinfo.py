"""
System module to collect CPU and memory information from server.
"""
from runners.runner import Runner
from constants import CPU_MEM_EMOJI, SMALL_WHITE_SQUARE_POINT


def format_system_info(raw_info: str) -> str:
    """
    Format raw system information into a readable format.
    
    Args:
        raw_info (str): Raw output from top command
        
    Returns:
        str: Formatted system information with bullet points
    """
    return "\n".join([
        f'{SMALL_WHITE_SQUARE_POINT} {line}'
        for line in raw_info.split('\n')
        if line.strip()
    ])


async def collect(runner: Runner) -> str:
    """
    Collect CPU and memory usage information.
    
    Args:
        runner (Runner): Runner instance to execute commands
        
    Returns:
        str: Formatted message containing CPU and memory information
    """
    command = 'top -b -n 1 | grep "%Cpu(s)\\|MiB Mem"'
    raw_info = await runner.run(command)
    
    formatted_info = format_system_info(raw_info)
    return f"- <b>CPU and memory info {CPU_MEM_EMOJI}:</b>\n{formatted_info}\n"
