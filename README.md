# VPS monitoring

## How to use

### Environment variables

Put `.env` file to `monitoring/` directory. This file must contain following variables:
```bash
TELEGRAM_BOT_USERNAME=@<bot username>  # username you get whrn registering bot
TELEGRAM_ACCESS_TOKEN=<telegram bot token>  # token you get when registering bot
SERVERS_CONFIG=servers.yml  # can use any path you want
ALLOWED_USERS=<chat id 1>,<chat id 2>,<group id 1>  # chat ids allowed to communicate with bot
DEFAULT_CHECK_INTERVAL=3600  # default interval at which bot will send scheduled messages
```

`SERVERS_CONFIG` points to `servers.yml` file (you can use any path you want). 

### Servers configuration

Example of `servers.yml` contents:

```yaml
servers:
  - ip: 192.168.0.1
    name: host1
    ssh:
      ssh_port: 22
      ssh_user: 'user'
      ssh_privkey_path: '/path/to/private/ssh/key'
    modules:
      - 'sysinfo'
      - 'wg'
  
  - ip: 192.168.0.2
    name: host2
    ssh:
      ssh_port: 22
      ssh_user: 'user'
      ssh_privkey_path: '/path/to/private/ssh/key'
    modules:
      - 'sysinfo'
      - 'ol'
      - 'wg'

  - ip: localhost
    name: host3
    modules:
      - 'sysinfo'
      - 'ol'

  # This is invalid - ssh is required for remote connection
  # This will be skipped and error shown in log
  - ip: 192.168.0.100
    name: somehost
    modules:
      - 'sysinfo'
```

> If no ssh connection info is present and ip is localhost/127.0.0.1, server will execute command on same host
> If host is not local and no ssh clock is present - this config entry will be skipped and error will appear in logs

### Commands at telegram bot

In telegram bot following commands must be setup (text below can be given to BotFather to setup all commands):
```
start - Get welcome message
help - Get commands info
getdata - Gather data from servers
set - Set scheduled messages in chat
unset - Remove scheduled messages from chat
getshedule - Get list of existing shedules
```

### Commands explained

`/start` and `/help` commands are standart commands to get info about bot and commands.

`/getdata` - can be used to get all monitoring data.

You also can set bot to send sheduled messages with monitoring data.

`/set` command accepts optional parameter - time in seconds. If no parameter is provided - default value from `DEFAULT_CHECK_INTERVAL` is used (you can set any).

For example, to set sheduled messages every 30 seconds in current chat or group (from where you communicate with bot) you can use command `/set 30`.

To stop scheduled messages in current chat (from where you communicate with bot) use command `/unset`.

To list all schedules (including shedules from other chats or groups) use `/getshedule`.


### Custom Modules

In `server.yml` `modules` parameter points to modules used to collect data.

This param must be the same as file name in `monitoring/modules/` directory.

You can add your own modules for your own services.

To do that all you have to do is to create file in `monitoring/modules/`, forexample `mymodule.py`

Inside this method you have to implement function `async def collect`:
```python
from runners.runner import Runner


async def collect(runner: Runner) -> str:
    command = 'ls /opt'
    # you have access to runner.run() asyncronous function
    result = await runner.run(command)
    # after that you can parce output of command and form string which will be then sent to chats
    return result
```
> IMPORTANT: try not to block code execution with heavy calculations. If possible, try to use async functions and await statements.

Inside function you have access to `runner.run` method which will execute your command in shell. This runner is set to communicate with target server via ssh (`asyncssh`) if you are monitoring remote server, or via asyncio subprocess if you are monitorin localhost.

You have to return string which has all formatted output you want to show in telegram bot, so feel free to stylise it.

> NOTE: HTTP parser is used in bot, so markdown cannot be used here.

