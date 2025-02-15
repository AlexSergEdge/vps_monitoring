# System module to collect system info from server
from ssh.runner import Runner

WG_EMOJI = '\U0001f5ff'
GREEN_ROUND_EMOJI = '\U0001f7e2'
RED_ROUND_EMOJI = '\U0001f534'


def wg_info_result_to_json(result):
    interfaces = []
    current_interface = None
    current_peer = None

    for line in result.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("interface:"):
            interface_name = line.split(":", 1)[1].strip()
            current_interface = {
                "interface": interface_name,
                "peers": []
            }
            interfaces.append(current_interface)
            current_peer = None
        elif line.startswith("peer:"):
            if current_interface is None:
                raise ValueError("Peer defined before any interface.")
            peer_name = line.split(":", 1)[1].strip()
            peer_details = {'peer': peer_name}
            current_interface["peers"].append(peer_details)
            current_peer = peer_details
        else:
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value.isdigit():
                value = int(value)
            elif key == "allowed ips":
                value = [ip.strip() for ip in value.split(",")]
            if current_peer is not None:
                current_peer[key] = value
            elif current_interface is not None:
                current_interface[key] = value
    return interfaces


async def collect(runner: Runner):

    message = f'- WG status info {WG_EMOJI}:\n'
    command = 'wg show'
    result = await runner.run(command)

    if result:
        message += f'{GREEN_ROUND_EMOJI} Running'
    else:
        message += f'{RED_ROUND_EMOJI} Not running'
        return message

    result_list = wg_info_result_to_json(result)
    for interface in result_list:
        message += f'\nInterface {interface['interface']}'
        for peer in interface['peers']:
            message += f'\nPeer {peer['peer']}, latest hadshake {peer.get('latest handshake', 'unknown')}, transfer {peer.get('transfer', 'unknown')}'

    return message



    