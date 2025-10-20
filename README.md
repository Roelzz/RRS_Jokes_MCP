# 🎭 Joke MCP Server for Microsoft Copilot Studio

A production-ready Model Context Protocol (MCP) server that provides joke tools to Microsoft Copilot Studio using **FastMCP 2.0** with **Streamable HTTP transport**.

[![FastMCP](https://img.shields.io/badge/FastMCP-2.0-blue)](https://gofastmcp.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)
[![Copilot Studio](https://img.shields.io/badge/Copilot%20Studio-Compatible-purple)](https://www.microsoft.com/microsoft-copilot/microsoft-copilot-studio)

---

## 📁 Files Included

| File | Purpose |
|------|---------|
| `joke_mcp_server.py` | Main MCP server with HTTP and STDIO support |
| `joke_mcp_schema.yaml` | OpenAPI schema for Copilot Studio connector |
| `requirements.txt` | Python dependencies |
| `test_all.py` | Comprehensive test suite (all transports) |
| `test_http.py` | Simple HTTP endpoint test |
| `QUICKSTART.md` | **⚡ 5-minute setup guide** |
| `COPILOT_STUDIO_SETUP.md` | **📖 Complete setup documentation** |
| `PRODUCTION_DEPLOYMENT.md` | 🚀 Production deployment guide |

---

## 🚀 Quick Start (5 Minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python joke_mcp_server.py
```

Output:
```
Starting Joke MCP Server with HTTP transport on http://localhost:8000/mcp
```

### 3. Test It
```bash
# Simple test
python test_http.py

# Comprehensive test
python test_all.py
```

### 4. Connect to Copilot Studio
See **[QUICKSTART.md](QUICKSTART.md)** for step-by-step instructions.

---

## 🎯 What This Server Does

Your Copilot will gain access to **4 joke tools**:

| Tool | Description | Example |
|------|-------------|---------|
| `get_random_joke` | Random joke from any category | "Tell me a joke" |
| `get_joke_by_category` | Joke from specific category | "Give me a programming joke" |
| `get_multiple_jokes` | Get 1-10 jokes at once | "Tell me 5 jokes" |
| `list_joke_categories` | List available categories | "What jokes do you have?" |

**Plus 1 resource:**
- `joke://stats` - Statistics about the joke collection

---

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes ⚡
- **[COPILOT_STUDIO_SETUP.md](COPILOT_STUDIO_SETUP.md)** - Complete setup guide 📖
- **[PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md)** - Deploy to production 🚀

---

## 🎮 Usage Examples

Once connected to Copilot Studio, users can:

**User:** "Tell me a joke"
**Copilot:** 😄 Why do programmers prefer dark mode? Because light attracts bugs!

**User:** "Give me a dad joke"
**Copilot:** 😄 What do you call a fake noodle? An impasta!

**User:** "Tell me 3 random jokes"
**Copilot:** *Returns 3 jokes from various categories*

---

## 🔧 Architecture

```
Microsoft Copilot Studio
         ↓ HTTPS (MCP Streamable)
  joke_mcp_server.py (Port 8000)
         ↓
    FastMCP Server
    ├── 4 Tools
    │   ├── get_random_joke
    │   ├── get_joke_by_category
    │   ├── get_multiple_jokes
    │   └── list_joke_categories
    └── 1 Resource
        └── joke://stats
```

---

## ⚙️ Configuration

### HTTP Transport (Default - for Copilot Studio)
```bash
python joke_mcp_server.py
# Runs on http://0.0.0.0:8000/mcp
```

### STDIO Transport (for Claude Desktop)
```bash
python joke_mcp_server.py --stdio
```

### Custom Port
Edit `joke_mcp_server.py`:
```python
mcp.run(transport="http", host="0.0.0.0", port=9000, path="/mcp")
```

---

## 🧪 Testing

### Quick HTTP Test
```bash
python test_http.py
```

### Full Test Suite
```bash
python test_all.py
```

Tests include:
- ✅ In-memory transport (unit testing)
- ✅ HTTP transport (Copilot Studio)
- ✅ STDIO transport (Claude Desktop)

### Manual Testing with curl
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":1}'
```

---

## 🔌 Connecting to Copilot Studio

### Step 1: Create Custom Connector
1. Open Microsoft Copilot Studio
2. Go to Tools → Add a tool → New tool → Custom connector
3. In Power Apps: New custom connector → Import OpenAPI file
4. Upload `joke_mcp_schema.yaml`
5. Update host field (localhost:8000 for testing)
6. Create connector

### Step 2: Add to Your Agent
1. Back in Copilot Studio: Tools → Add a tool
2. Select "Model Context Protocol"
3. Choose "Joke MCP Server"
4. Click "Add to agent"

**Detailed instructions:** See [COPILOT_STUDIO_SETUP.md](COPILOT_STUDIO_SETUP.md)

---

## 🌐 Production Deployment

Deploy to:
- **Azure App Service** (Recommended for Microsoft ecosystem)
- **AWS EC2/Lambda**
- **Google Cloud Run**
- **Docker/Kubernetes**
- **Railway** (Easiest)

**Full guide:** See [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md)

### Quick Deploy to Azure
```bash
az webapp up --name my-joke-server --runtime "PYTHON:3.11"
```

Update `joke_mcp_schema.yaml` with your domain:
```yaml
host: my-joke-server.azurewebsites.net
schemes:
  - https
```

---

## 🔒 Security

### For Production:
1. ✅ Use HTTPS only
2. ✅ Add authentication
3. ✅ Enable rate limiting
4. ✅ Use environment variables for secrets
5. ✅ Monitor and log all requests

### Adding Authentication
```python
import os
from fastmcp import FastMCP

mcp = FastMCP(
    "Joke Server",
    auth={"api_key": os.environ.get("MCP_API_KEY")}
)
```

---

## 🛠️ Customization

### Adding Your Own Jokes

Edit `joke_mcp_server.py`:

```python
PROGRAMMING_JOKES = [
    {
        "setup": "Your question",
        "punchline": "Your answer"
    },
    # Add more...
]
```

### Adding New Categories

1. Create new joke list
2. Update `get_joke_by_category()`
3. Update `list_joke_categories()`
4. Update `get_random_joke()` to include new category

---

## 📊 Key Features

✨ **FastMCP 2.0** - Modern, Pythonic MCP framework
🔄 **Dual Transport** - Supports both HTTP and STDIO
🎯 **Copilot Studio Ready** - OpenAPI schema included
🧪 **Comprehensive Tests** - Multiple test suites
📖 **Full Documentation** - Setup, testing, and deployment guides
🔒 **Production Ready** - Security and performance best practices
🚀 **Easy Deployment** - Multiple cloud platform guides

---

## 🐛 Troubleshooting

### Server Won't Start
```bash
# Check Python version (need 3.10+)
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Can't Connect from Copilot Studio
1. ✅ Ensure server is running
2. ✅ Verify firewall allows port 8000
3. ✅ Check that Generative Orchestration is enabled
4. ✅ Confirm custom connector is properly configured

### Tests Failing
```bash
# Check if server is running
curl http://localhost:8000/mcp

# View server logs
# (check terminal where server is running)
```

**More help:** See [COPILOT_STUDIO_SETUP.md](COPILOT_STUDIO_SETUP.md#troubleshooting)

---

## 📦 Requirements

- **Python:** 3.10 or higher
- **FastMCP:** 2.0.0 or higher
- **Requests:** 2.31.0 or higher (for testing)
- **Copilot Studio:** Generative Orchestration enabled

---

## 📖 Additional Resources

- **FastMCP Documentation:** https://gofastmcp.com/
- **FastMCP GitHub:** https://github.com/jlowin/fastmcp
- **MCP Specification:** https://modelcontextprotocol.io
- **Copilot Studio MCP Guide:** https://learn.microsoft.com/microsoft-copilot-studio/agent-extend-action-mcp

---

## 🤝 Contributing

This is a sample/template project. Feel free to:
- Fork and customize for your needs
- Add more joke categories
- Extend with additional tools
- Deploy to your infrastructure

---

## 📝 License

This is a demonstration/sample project. Use and modify as needed for your purposes.

---

## 🎉 Success Checklist

Before going live, ensure:

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Server starts without errors
- [ ] Tests pass (`python test_all.py`)
- [ ] YAML schema updated with your domain
- [ ] Custom connector created in Copilot Studio
- [ ] Connector added to your agent
- [ ] Test conversation successful
- [ ] (Production) Deployed to cloud platform
- [ ] (Production) HTTPS enabled
- [ ] (Production) Monitoring configured

---

## 🚀 Next Steps

1. **Test Locally** - Run through [QUICKSTART.md](QUICKSTART.md)
2. **Connect to Copilot** - Follow [COPILOT_STUDIO_SETUP.md](COPILOT_STUDIO_SETUP.md)
3. **Deploy to Production** - Use [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md)
4. **Customize** - Add your own jokes and tools!

---

**Ready to make your Copilot tell jokes? Let's go! 🎭😄**

Questions? Check the troubleshooting sections in the documentation files.
