from runners.runner import Runner

# Emojis for prettier text
DRAGON_EMOJI = '\U0001F409'
GREEN_ROUND_EMOJI = '\U0001f7e2'
RED_ROUND_EMOJI = '\U0001f534'

# TODO: provide verbose as option for collect functions to get more data
VERBOSE = False


def wg_info_result_to_json(result):
    # Convert plain text output of wg show command into json
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
            # If new interface is found - current peer resets
            current_peer = None
        elif line.startswith("peer:"):
            if current_interface is None:
                raise ValueError("Peer defined before any interface.")
            peer_name = line.split(":", 1)[1].strip()
            peer_details = {'peer': peer_name}
            current_interface["peers"].append(peer_details)
            current_peer = peer_details
        else:
            # if no key value is present - skip
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value.isdigit():
                value = int(value)
            # Allowed ips are respresented as list
            elif key == "allowed ips":
                value = [ip.strip() for ip in value.split(",")]
            # Save current peer params
            if current_peer is not None:
                current_peer[key] = value
            # Save current interface params (current peer is None)
            elif current_interface is not None:
                current_interface[key] = value
    
    return interfaces


async def collect(runner: Runner) -> str:
    message = f'- <b>WG status info {DRAGON_EMOJI}:</b>\n'
    command = 'wg show'
    result = await runner.run(command)

    if not result:
        message += f'{RED_ROUND_EMOJI} Not running :(\n'
        return message
    
    message += f'{GREEN_ROUND_EMOJI} Running :)\n'

    # TODO: provide this as option (now it is hardcoded into False)
    # now it is turned off, just status of wg itself showed
    if VERBOSE:
        result_list = wg_info_result_to_json(result)
        for interface in result_list:
            message += f'\n<b>{interface['interface']} interface</b> peers:'
            for peer in interface['peers']:
                message += f'\n - <b>{peer['peer'][:6]}...</b>'
                if peer.get('latest handshake') and peer.get('transfer'):
                    message += f' : <code>{peer['transfer']}, latest handshake {peer['latest handshake']}</code>'

    return message



    