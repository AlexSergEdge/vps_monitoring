import json
from datetime import datetime

from runners.runner import Runner


# TODO: provde as option
VERBOSE = False

GLOBE_EMOJI = '\U0001F310'

GREEN_ROUND_EMOJI = '\U0001f7e2'
RED_ROUND_EMOJI = '\U0001f534'

GREEN_CHECK_EMOJI = '\U00002705'
RED_CROSS_EMOJI = '\U0000274C'

def convert_date(date_str):
    # we convert date from fromat with ms after ., but we do not need part after .
    dt = datetime.strptime(date_str.split('.')[0], '%Y-%m-%dT%H:%M:%S')
    return dt.strftime('%H:%M:%S %d-%m-%Y')


async def collect(runner: Runner):

    result = f'- <b>OL status info {GLOBE_EMOJI}:</b>\n'

    # Two containers have to be running
    containers = (
        'shadowbox',
        'watchtower'
    )

    # Var to store OL status (if any of containers is down - OL is down)
    ol_up = True

    for container in containers:
        container_info = await runner.run(f'docker inspect {container}')
        container_status = f'Container {container}: '

        if not container_info or 'Error: No such object:' in container_info:
            container_status = f'{RED_CROSS_EMOJI} ' + container_status + f' does not exist\n'
            ol_up = False
        else:
            container_info = json.loads(container_info)
            
            state = container_info[0].get('State')
        
            if state.get('Status') != 'running':
                ol_up = False
                container_status = f'{RED_CROSS_EMOJI} ' + container_status + f' is not running\n'
                
                # We do not need this excessive info, if it is present
                # If container is down we show info as json
                if state.get('Health'):
                    del state['Health']
                container_status += f'<code>{json.dumps(state, indent=4)}</code>\n'
            else:
                container_status = f'{GREEN_CHECK_EMOJI} '+ container_status + f' is up'
                # If container is up - just show when it was started
                container_status += f' (started: {convert_date(state['StartedAt'])})\n'
                
        if VERBOSE:
            result += container_status

    if not ol_up:
        result += f'{RED_ROUND_EMOJI} OL is down :(\n'
    else:
        result += f'{GREEN_ROUND_EMOJI} OL is up :)\n'
    
    return result
        

        