import asyncio
import asyncssh
import sys
from loguru import logger


# TODO: add run for later implementation
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
                logger.error(f"{exc.stderr}")
                logger.error(f'Process exited with status {exc.exit_status}')


class LocalRunner(Runner):

    async def run(self, command: str) -> None:
        process = await asyncio.create_subprocess_shell(
            command,  # Note that running command as non-root may result in Permission denied erorr or password prompt (if command has sudo) 
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            logger.error(f'Process exited with error: {stderr.decode()}')
            return None  # TODO: think how to better handle situations when command exists but returns None, and when there is error

        return stdout.decode()
