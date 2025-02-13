import asyncio
import asyncssh
import sys


class RemoteRunner():

    def __init__(self, ip_addr, port, username, key):
        self.ip_addr = ip_addr
        self.port = port
        self.username = username
        self.key = key

    async def run(self, command: list) -> None:
        command = " ".join(command)
        async with asyncssh.connect(self.ip_addr, port=self.port, username=self.username
                                    , client_keys=[self.key]) as conn:
            try:
                result = await conn.run(command, check=True)
                return result.stdout
            except asyncssh.ProcessError as exc:
                print(exc.stderr, end='')
                print(f'Process exited with status {exc.exit_status}', file=sys.stderr)


class LocalRunner():

    async def run(self, command: list) -> None:
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            print(f'Process exited with error: {stderr.decode()}')

        return stdout.decode()


# Usage:

# local_runner = LocalRunner()
# res = asyncio.run(local_runner.run(['ls', '/opt']))
# print(res)

# remote_runner = RemoteRunner('xxx.xxx.xxx.xxx', 33, 'root', '/path/to/key')
# res = asyncio.run(remote_runner.run(['ls', '/opt']))
# print(res)