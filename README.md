# CDP-to-MCP Gateway

Local Python daemon connecting your active Google Chrome browser (via Chrome DevTools Protocol) to a Model Context Protocol (MCP) server so local AI agents can control your browser seamlessly.

## Quickstart

1. Launch Chrome with Remote Debugging Enabled:
```bash
# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222

# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the MCP Gateway:
```bash
python main.py
```

## Features
- **Zero Login Re-auth**: Connects directly to your human-authenticated Chrome tab.
- **LLM-Optimized DOM**: Strips script tags, hidden elements, SVGs, and presents interactive elements with simple sequential IDs `[e1]`, `[e2]`.
- **FastMCP Standard Tools**: `read_page`, `click_element`, `fill_input`, `navigate`.
