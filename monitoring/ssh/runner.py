import asyncio
import asyncssh
import sys

async def run_client(ip_addr, port, username, key, command) -> None:
    async with asyncssh.connect(ip_addr, port=port, username=username, client_keys=[key]) as conn:
        try:
            result = await conn.run(command, check=True)
            return result.stdout
        except asyncssh.ProcessError as exc:
            print(exc.stderr, end='')
            print(f'Process exited with status {exc.exit_status}', file=sys.stderr)

# example run
# def run():
#     try:
#         asyncio.run(run_client('x.x.x.x', 22, 'root', '/path/to/key', 'ls /opt'))
#     except (OSError, asyncssh.Error) as exc:
#         sys.exit('SSH connection failed: ' + str(exc))