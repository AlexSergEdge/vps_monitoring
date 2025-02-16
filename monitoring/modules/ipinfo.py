"""
System module to collect IP address information from server.
"""
from runners.runner import Runner


async def collect(runner: Runner) -> str:
    """
    Collect the primary IP address of the server.
    
    Args:
        runner (Runner): Runner instance to execute commands
        
    Returns:
        str: The primary IP address of the server
    """
    command = "hostname -I | awk '{print $1}'"
    ip_address = await runner.run(command)
    return ip_address.rstrip()
