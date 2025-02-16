from runners.runner import Runner
from constants import DRAGON_EMOJI, GREEN_ROUND_EMOJI, RED_ROUND_EMOJI, WG_VERBOSE


def wg_info_result_to_json(result: str) -> list:
    """
    Convert plain text output of WireGuard show command into structured JSON format.
    
    Args:
        result (str): Raw output from 'wg show' command
        
    Returns:
        list: List of dictionaries containing interface and peer information
        
    Raises:
        ValueError: If peer is defined before any interface
    """
    interfaces = []
    current_interface = None
    current_peer = None

    for line in result.splitlines():
        line = line.strip()
        if not line:
            continue

        # Handle interface definition
        if line.startswith("interface:"):
            current_interface = {
                "interface": line.split(":", 1)[1].strip(),
                "peers": []
            }
            interfaces.append(current_interface)
            current_peer = None
            continue

        # Handle peer definition
        if line.startswith("peer:"):
            if current_interface is None:
                raise ValueError("Peer defined before any interface.")
            current_peer = {'peer': line.split(":", 1)[1].strip()}
            current_interface["peers"].append(current_peer)
            continue

        # Handle key-value pairs
        if ":" not in line:
            continue
            
        key, value = [part.strip() for part in line.split(":", 1)]
        
        # Process value based on type
        if value.isdigit():
            value = int(value)
        elif key == "allowed ips":
            value = [ip.strip() for ip in value.split(",")]
            
        # Add to appropriate dictionary
        target_dict = current_peer if current_peer is not None else current_interface
        if target_dict is not None:
            target_dict[key] = value
    
    return interfaces


async def collect(runner: Runner) -> str:
    """
    Collect WireGuard status information from the system.
    
    Args:
        runner (Runner): Runner instance to execute commands
        
    Returns:
        str: Formatted message containing WireGuard status
    """
    message = f'- <b>WG status info {DRAGON_EMOJI}:</b>\n'
    result = await runner.run('wg show')

    if not result:
        return message + f'{RED_ROUND_EMOJI} Not running :(\n'
    
    message += f'{GREEN_ROUND_EMOJI} Running :)\n'

    if WG_VERBOSE:
        interfaces = wg_info_result_to_json(result)
        for interface in interfaces:
            message += f'\n<b>{interface["interface"]} interface</b> peers:'
            for peer in interface["peers"]:
                peer_info = f'\n - <b>{peer["peer"][:6]}...</b>'
                
                if peer.get('latest handshake') and peer.get('transfer'):
                    peer_info += f' : <code>{peer["transfer"]}, latest handshake {peer["latest handshake"]}</code>'
                
                message += peer_info

    return message



    