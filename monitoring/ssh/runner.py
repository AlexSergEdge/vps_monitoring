import asyncio
import asyncssh
import sys


class Runner():
    pass


class RemoteRunner(Runner):

    def __init__(self, ip_addr, port, username, key):
        self.ip_addr = ip_addr
        self.port = port
        self.username = username
        self.key = key

    async def run(self, command: str) -> None:
        async with asyncssh.connect(self.ip_addr, port=self.port, username=self.username
                                    , client_keys=[self.key]) as conn:
            try:
                result = await conn.run(command, check=True)
                return result.stdout
            except asyncssh.ProcessError as exc:
                print(exc.stderr, end='')
                print(f'Process exited with status {exc.exit_status}', file=sys.stderr)


class LocalRunner(Runner):

    async def run(self, command: str) -> None:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            print(f'Process exited with error: {stderr.decode()}')

        return stdout.decode()
