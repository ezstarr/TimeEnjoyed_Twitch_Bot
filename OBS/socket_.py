"""
Copyright (c) 2024 - Present (Mysty)<evieepy@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from __future__ import annotations

import asyncio
import logging

import simpleobsws

logger: logging.Logger = logging.getLogger(__name__)


class OBSWebsocket:
    
    def __init__(
        self,
        host: str,
        port: int,
        *,
        password: str,
        ) -> None:
        self._host = host
        self._port = port
        self._password = password
        
        url: str = f"ws://{host}:{port}"
        
        paramters: simpleobsws.IndentificationParameters = simpleobsws.IdentificationParameters(eventSubscriptions=None)
        self._socket: simpleobsws.WebSocketClient = simpleobsws.WebSocketClient(
            url=url,
            password=password,
            identification_parameters=paramters,
        )
        
        self._connected: bool = False
        self._listener_task: asyncio.Task[None] | None = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__qualname__} connected={self._connected}, host={self._host=}, port={self._port=}>"

    async def __aenter__(self) -> OBSWebsocket:
        await self.connect()
        return self
        
    async def __aexit__(self, *_) -> None:
        await self.close()
        
    async def connect(self, ) -> None:
        logger.info("Connecting to OBS at %s:%s", self._host, self._port)
        await self._socket.connect()
        await self._socket.wait_until_identified()
        
        self._connected = True
        logger.info("Successfully connected to OBS at %s:%s", self._host, self._port)
        
        self._listener_task = asyncio.create_task(self.listen(), name=f"{self.__class__.__qualname__} Listener")
        
    def _cancel_task(self) -> None:
        if self._listener_task and not self._listener_task.done():
            
            try:
                self._listener_task.cancel()
            except Exception:
                logger.info("Canceling listener for <%s> failed. Disregarding...", self.__class__.__qualname__)
                pass
        
        self._listener_task = None
        
    async def close(self, ) -> None:
        self._cancel_task()
        
        await self._socket.disconnect()
        self._socket = None
        
        logger.info("Successfully closed connection to OBS.")
        
    async def send(self, command: str, data: dict[str, str] = None) -> simpleobsws.RequestResponse:
        request: simpleobsws.Request = simpleobsws.Request(command, data)
        response: simpleobsws.RequestResponse = await self._socket.call(request)
        
        return response
    
    async def listen(self, ) -> None:
        logger.info("Started listener task for <%s>", self.__class__.__qualname__)
        # TODO: Listen for events...
