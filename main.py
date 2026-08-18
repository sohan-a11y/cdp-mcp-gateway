import asyncio
import signal
import sys
from cdp.connection import CDPManager
from mcp_server.server import mcp, set_cdp_manager
from logger import get_logger

logger = get_logger("main")

async def main():
    manager = CDPManager()
    await manager.connect()
    set_cdp_manager(manager)

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown(manager)))
        except NotImplementedError:
            pass

    logger.info("Starting CDP-to-MCP Gateway server on stdio transport...")
    try:
        await mcp.run_stdio_async()
    finally:
        await manager.close()

async def shutdown(manager: CDPManager):
    logger.info("Shutdown signal received. Closing CDP connection...")
    await manager.close()
    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
