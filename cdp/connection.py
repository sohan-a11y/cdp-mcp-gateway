import asyncio
from playwright.async_api import async_playwright, Browser, Page, Playwright
from config import settings
from logger import get_logger

logger = get_logger("cdp_connection")

class CDPManager:
    def __init__(self, cdp_url: str = settings.CHROME_CDP_URL):
        self.cdp_url = cdp_url
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None

    async def connect(self, retries: int = 3, delay: float = 2.0):
        self.playwright = await async_playwright().start()
        for attempt in range(1, retries + 1):
            try:
                logger.info(f"Connecting to Chrome CDP at {self.cdp_url} (Attempt {attempt}/{retries})")
                self.browser = await self.playwright.chromium.connect_over_cdp(self.cdp_url)
                logger.info("Successfully connected to Chrome via CDP")
                return
            except Exception as e:
                logger.warning(f"Connection failed: {e}")
                if attempt == retries:
                    raise RuntimeError(f"Could not connect to Chrome CDP at {self.cdp_url} after {retries} attempts.")
                await asyncio.sleep(delay * (2 ** (attempt - 1)))

    async def get_active_page(self) -> Page:
        if not self.browser:
            raise RuntimeError("CDPManager is not connected. Call connect() first.")
        contexts = self.browser.contexts
        if not contexts:
            raise RuntimeError("No active browser context found in Chrome.")
        context = contexts[0]
        pages = context.pages
        if not pages:
            page = await context.new_page()
            return page
        return pages[0]

    async def close(self):
        if self.browser:
            await self.browser.close()
            logger.info("Disconnected CDP session.")
        if self.playwright:
            await self.playwright.stop()
