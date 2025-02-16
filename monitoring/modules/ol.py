import json
from datetime import datetime
from typing import Dict, Optional

from runners.runner import Runner
from constants import (
    GLOBE_EMOJI, GREEN_ROUND_EMOJI, RED_ROUND_EMOJI,
    GREEN_CHECK_EMOJI, RED_CROSS_EMOJI, OL_VERBOSE,
    OL_CONTAINERS
)


def convert_date(date_str: str) -> str:
    """
    Convert ISO format date string to a more readable format.
    
    Args:
        date_str (str): Date string in ISO format with milliseconds
        
    Returns:
        str: Formatted date string in 'HH:MM:SS DD-MM-YYYY' format
    """
    dt = datetime.strptime(date_str.split('.')[0], '%Y-%m-%dT%H:%M:%S')
    return dt.strftime('%H:%M:%S %d-%m-%Y')


def get_container_status(container_info: Optional[str], container_name: str) -> tuple[str, bool]:
    """
    Process container information and return its status.
    
    Args:
        container_info (Optional[str]): Docker inspect output for the container
        container_name (str): Name of the container
        
    Returns:
        tuple[str, bool]: Tuple containing (status message, is_container_up)
    """
    status_prefix = f'Container {container_name}: '
    
    if not container_info or 'Error: No such object:' in container_info:
        return f'{RED_CROSS_EMOJI} {status_prefix} does not exist\n', False
        
    container_data = json.loads(container_info)[0]
    state: Dict = container_data.get('State', {})
    
    if state.get('Status') != 'running':
        # Remove health info for non-running containers to keep output clean
        if state.get('Health'):
            del state['Health']
        return (
            f'{RED_CROSS_EMOJI} {status_prefix}is not running\n'
            f'<code>{json.dumps(state, indent=4)}</code>\n',
            False
        )
    
    return (
        f'{GREEN_CHECK_EMOJI} {status_prefix}is up '
        f'(started: {convert_date(state["StartedAt"])})\n',
        True
    )


async def collect(runner: Runner) -> str:
    """
    Collect Outline VPN status information.
    
    Args:
        runner (Runner): Runner instance to execute commands
        
    Returns:
        str: Formatted message containing Outline VPN status
    """
    result = f'- <b>OL status info {GLOBE_EMOJI}:</b>\n'
    ol_up = True
    
    for container in OL_CONTAINERS:
        container_info = await runner.run(f'docker inspect {container}')
        status_message, container_up = get_container_status(container_info, container)
        
        if OL_VERBOSE:
            result += status_message
        
        ol_up = ol_up and container_up
    
    status_emoji = GREEN_ROUND_EMOJI if ol_up else RED_ROUND_EMOJI
    status_text = 'up' if ol_up else 'down'
    result += f'{status_emoji} OL is {status_text} {"" if ol_up else ":("}\n'
    
    return result
        

        