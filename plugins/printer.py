import asyncio
import functools
import io
import logging
import sys
import time
from functools import partial

# GIVEN:
  # Printer needs to be async
  # run a loop with a blocking queue (asyncio.queue)
import async_timeout
import bluetooth
from PIL import Image, ImageOps, ImageEnhance, ImageDraw

# Define logging format and set up logging
LFORMAT: str = f"%(levelname)s:{'':>4}\x1b[0m \x1b[34m%(name)s\x1b[0m %(message)s \x1b[37;1m%(asctime)s\x1b[0m"
# DFORMAT: str = f"%Y-%m-%d %H:%M:%S"

logging.basicConfig(format=LFORMAT, level=logging.INFO)
logger: logging.Logger = logging.getLogger("Thermal.Printer")
logger.setLevel(level=logging.INFO)

# Maximum height for images to be processed
MAX_HEIGHT: int = 65535

class Printer:

    def __init__(self, *, host: str) -> None:
        # Initialize printer with host address
        self.host = host
        
        # Create a lock for thread-safe operations
        self._lock: asyncio.Lock = asyncio.Lock()
        # Create a Bluetooth socket for communication
        self._socket: bluetooth.BluetoothSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    async def receive(self, timeout: int = 10, /) -> str:
        # Receive data from the printer with a timeout
        try:
            async with async_timeout.timeout(timeout):
                data: str = await asyncio.to_thread(self._receive)
        except asyncio.TimeoutError:
            logger.warning("Receiving data from the printer blocked for too long.")
            return ""

        return data

    def _receive(self, size: int = 1024) -> str:
        # Receive raw bytes from the printer and decode them
        data: bytes = self._socket.recv(size)

        try:
            decoded: str = data.decode()
        except UnicodeError:
            logger.warning("Unable to decode bytes received from the printer.")
            return ""

        return decoded

    async def _send(self, __value: bytes, /, *, recv: bool = False) -> str | None:
        # Send data to the printer and optionally receive a response
        self._socket.send(__value)

        if not recv:
            return

        data: str = await self.receive()
        return data

    async def send_command(self, __value: str | bytes, /, *, recv: bool = False) -> str | None:
        # Send a command to the printer, either as a string or bytes
        command: bytes
        if isinstance(__value, str):
            command = bytes.fromhex(__value)
        else:
            command = __value

        data: str | None = await self._send(command, recv=recv)
        return data

    async def get_device_name(self) -> None:
        # Send a command to the printer, either as a string or bytes
        async with self._lock:
            data: str | None = await self.send_command("10ff3011", recv=True)
            logger.info('Device NAME: %s', data)

    async def get_FWDPI(self) -> None:
        # Retrieve the device's FWDPI
        async with self._lock:
            data: str | None = await self.send_command("10ff20f1", recv=True)
            logger.info('Device FWDPI: %s', data)

    async def get_serial(self) -> None:
        # Retrieve the device's serial number
        async with self._lock:
            data: str | None = await self.send_command("10ff20f2", recv=True)
            logger.info('Device SERIAL: %s', data)

    async def reset(self) -> None:
        # Reset the printer
        async with self._lock:
            data: str | None = await self.send_command("10ff50f1", recv=True)
            await self.send_command("000000000000000000000000", recv=False)

            logger.info('Device RESET v1: %s', data)

    async def reset_two(self) -> None:
        # Alternative reset method
        async with self._lock:
            await self.send_command("10fffe01", recv=False)
            await self.send_command("\n", recv=False)

    def load_image(self, fp: io.BufferedIOBase | str | bytes) -> Image:
        # Load an image from a file, string, or bytes
        try:
            image: Image = Image.open(fp)
        except Exception as e:
            raise IOError from e

    def _process_image(
            self,
            fp: str | io.BufferedIOBase | bytes,
            /,
            *,
            brightness: float | None = None,
            contrast: float | None = None
    ) -> tuple[bytes, io.BytesIO]:
        # Process an image for printing, adjusting brightness and contrast
        image: Image = Image.open(fp)
        image = image.convert("L")

        width: int = image.size[0]
        height: int = image.size[1]

        if brightness:
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness)

        if contrast:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(contrast)

        image = ImageOps.invert(image)

        new_width = 384  # A6 image width
        scale: float = new_width / float(width)
        new_height: int = int(height * scale)

        if new_height > MAX_HEIGHT:
            raise ValueError("Unable to process this image as it is too large.")

        image = image.resize((384, new_height), Image.ANTIALIAS)
        image = image.convert("1")

        hbytes: bytes = new_height.to_bytes(2, byteorder="little")
        ibytes: io.BytesIO = io.BytesIO(image.tobytes())
        ibytes.seek(0)

        return hbytes, ibytes

    async def print_image(
            self,
            fp: str | io.BufferedIOBase | bytes,
            *,
            brightness: float | None = None,
            contrast: float | None = None,
            feed: bool = True
    ) -> None:
        async with self._lock:
            # TODO: Remove this with keep-alive...
            try:
                await self.connect()
            except OSError:
                pass

            data: tuple[bytes, io.BytesIO]

            partial = functools.partial(self._process_image, fp, brightness=brightness, contrast=contrast)
            data = await asyncio.to_thread(partial)

            CHUNK_SIZE: int = 122

            await self.send_command("10fffe01", recv=False)
            await self.send_command("000000000000000000000000", recv=False)

            hbytes: bytes = bytes.fromhex("1d7630003000") + data[0]
            ibytes: io.BytesIO = data[1]
            buffer: bytes = ibytes.getbuffer().tobytes()

            await self.send_command(hbytes, recv=False)

            logger.info("Beginning Printing %d Chunks...", len(buffer) / CHUNK_SIZE)
            for i in range(0, len(buffer), CHUNK_SIZE):
                chunk: bytes = buffer[i:i + CHUNK_SIZE]

                await self.send_command(chunk, recv=False)
                await asyncio.sleep(0.02)

            if feed:
                logger.info("Feeding Printer...")

                empty: list[int] = [0] * 122
                for i in range(1, 35):

                    await self.send_command(bytes(empty), recv=False)
                    await asyncio.sleep(0.02)

            await self.send_command("1b4a4010fffe45", recv=False)
            logger.info("Finished Printing!")

    def _connect(self) -> None:
        self._socket.connect((self.host, 1))

    async def connect(self) -> None:
        # TODO: Add a keep-alive...

        await asyncio.to_thread(self._connect)
        await self.get_device_name()
        await self.get_FWDPI()
        await self.get_serial()

        # Reset the device...
        await self.reset()

    async def send(self, __value: bytes, /, *, recv: bool = False) -> None:
        data: str | None = await self._send(__value, recv=recv)

        if data:
            logger.info(f"Received Data from Send: %s", data)



