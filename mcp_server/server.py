from mcp.server.fastmcp import FastMCP
from cdp.connection import CDPManager
from cdp.tree_parser import extract_clean_accessibility_tree
from config import settings
from logger import get_logger

logger = get_logger("mcp_server")

mcp = FastMCP(settings.MCP_SERVER_NAME)
cdp_manager: CDPManager | None = None
latest_element_map: dict[str, str] = {}

def set_cdp_manager(manager: CDPManager):
    global cdp_manager
    cdp_manager = manager

@mcp.tool()
async def read_page() -> str:
    """Returns the current page's simplified UI tree with interactive element IDs."""
    global latest_element_map
    if not cdp_manager:
        return "Error: CDP Manager not initialized."
    page = await cdp_manager.get_active_page()
    data = await extract_clean_accessibility_tree(page)
    latest_element_map = data.get("map", {})
    return f"Page Title: {data.get('title')}\n\nUI Tree:\n{data.get('tree')}"

@mcp.tool()
async def click_element(element_id: str) -> str:
    """Clicks an interactive element by its sequential ID (e.g. e1, e2)."""
    if not cdp_manager:
        return "Error: CDP Manager not initialized."
    clean_id = element_id.lstrip("[").rstrip("]").strip()
    selector = latest_element_map.get(clean_id)
    if not selector:
        return f"Error: Element ID '{element_id}' not found in recent page state. Call read_page first."
    page = await cdp_manager.get_active_page()
    try:
        await page.click(selector, timeout=settings.ACTION_TIMEOUT * 1000)
        return f"Successfully clicked element [{clean_id}] ({selector})"
    except Exception as e:
        return f"Failed to click element [{clean_id}]: {e}"

@mcp.tool()
async def fill_input(element_id: str, text: str) -> str:
    """Fills an input/textarea element by its sequential ID with specified text."""
    if not cdp_manager:
        return "Error: CDP Manager not initialized."
    clean_id = element_id.lstrip("[").rstrip("]").strip()
    selector = latest_element_map.get(clean_id)
    if not selector:
        return f"Error: Element ID '{element_id}' not found in recent page state. Call read_page first."
    page = await cdp_manager.get_active_page()
    try:
        await page.fill(selector, text, timeout=settings.ACTION_TIMEOUT * 1000)
        return f"Successfully filled text into element [{clean_id}]"
    except Exception as e:
        return f"Failed to fill element [{clean_id}]: {e}"

@mcp.tool()
async def navigate(url: str) -> str:
    """Navigates active Chrome tab to a target URL."""
    if not cdp_manager:
        return "Error: CDP Manager not initialized."
    page = await cdp_manager.get_active_page()
    try:
        await page.goto(url, wait_until="networkidle", timeout=settings.ACTION_TIMEOUT * 1000)
        return f"Successfully navigated to {url}"
    except Exception as e:
        return f"Failed to navigate to {url}: {e}"
