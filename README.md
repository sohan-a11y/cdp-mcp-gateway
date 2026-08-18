# CDP-to-MCP Gateway 🤖

![GitHub License](https://img.shields.io/github/license/sohan-a11y/cdp-mcp-gateway?style=flat-square)
![GitHub Last Commit](https://img.shields.io/github/last-commit/sohan-a11y/cdp-mcp-gateway?style=flat-square)
![GitHub Stars](https://img.shields.io/github/stars/sohan-a11y/cdp-mcp-gateway?style=flat-square)
![GitHub Forks](https://img.shields.io/github/forks/sohan-a11y/cdp-mcp-gateway?style=flat-square)


CDP-to-MCP Gateway: Connect active Chrome instances to Model Context Protocol (MCP) servers for LLM browser control.

---

## 🌟 Key Features

- 🌐 **Chrome DevTools Protocol Integration**: Direct control over human-authenticated desktop Chrome sessions.
- 🤖 **MCP Server Standard**: Exposes `read_page`, `click_element`, `fill_input`, `navigate` as standard tools.
- 📄 **LLM-Optimized DOM Parsing**: Strips noise, script tags, and SVGs, mapping interactive elements to element IDs `[e1]`, `[e2]`.
- 🔒 **No Auth Wall Bypass Needed**: Leverages your active login cookies seamlessly.

---

## 🛠️ Tech Stack

[![Skills](https://skillicons.dev/icons?i=python,chrome,fastapi)](https://skillicons.dev)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ / Node.js (depending on module)
- Git

### Installation
```bash
# Clone repository
git clone https://github.com/sohan-a11y/cdp-mcp-gateway.git
cd cdp-mcp-gateway

# Install dependencies (if python project)
pip install -r requirements.txt
```

---

## 💡 Usage Example

```bash
# Run application entrypoint
python main.py
```

---

## 🗺️ Roadmap & Future Enhancements
- [x] Initial release & core functionality
- [ ] Enterprise security integration
- [ ] Multi-tenant Cloud deployment support
- [ ] Advanced performance profiling

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to check the [issues page](https://github.com/sohan-a11y/cdp-mcp-gateway/issues).

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
