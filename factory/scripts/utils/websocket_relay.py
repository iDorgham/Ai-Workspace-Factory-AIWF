#!/usr/bin/env python3
"""
AIWF WebSocket Relay v1.0.0
Central hub for real-time factory telemetry and dashboard updates.
"""

import asyncio
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WS-RELAY")

class OmegaRelay:
    def __init__(self, host='127.0.0.1', port=9001):
        self.host = host
        self.port = port
        self.clients = set() # Connected dashboard clients
        self.workspaces = {} # workspace_id -> last_seen

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        logger.info(f"New connection from {addr}")
        self.clients.add(writer)

        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                
                message = json.loads(data.decode())
                msg_type = message.get("type")
                
                if msg_type == "LOG_STREAM":
                    # Broadcast log to all dashboard clients
                    await self.broadcast(message)
                elif msg_type == "HEALTH_PING":
                    self.workspaces[message.get("workspace")] = datetime.now().isoformat()
                    logger.info(f"Health ping from: {message.get('workspace')}")

        except Exception as e:
            logger.error(f"Error handling client {addr}: {e}")
        finally:
            logger.info(f"Connection closed for {addr}")
            self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()

    async def broadcast(self, message):
        """Send message to all connected dashboard clients."""
        if not self.clients:
            return
        
        data = (json.dumps(message) + "\n").encode()
        for client in self.clients:
            try:
                client.write(data)
                await client.drain()
            except:
                pass

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        logger.info(f"🛰️ Omega Relay serving on {addr}")

        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    relay = OmegaRelay()
    try:
        asyncio.run(relay.start())
    except KeyboardInterrupt:
        logger.info("Relay stopped by user.")
