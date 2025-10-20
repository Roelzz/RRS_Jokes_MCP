# Python-based MCP Server Tutorial - Deploy to Azure

A straightforward guide to building your first Model Context Protocol (MCP) server in Python, testing it locally, containerizing it with Podman, and deploying it to Azure Container Apps. No fluff. Just the steps that work.

This tutorial uses a joke server as an example, but the pattern works for any MCP server you want to build.

## What is MCP?

Model Context Protocol (MCP) is a standard that lets AI assistants connect to external tools and data sources. Think of it as a bridge between AI models and your custom functionality.

**MCP servers can provide:**
- **Tools** - Functions the AI can call (e.g., fetch data, perform calculations, trigger actions)
- **Resources** - Data the AI can read (e.g., files, databases, APIs)
- **Prompts** - Pre-built prompt templates for common tasks

Right now, you can connect MCP servers to Microsoft Copilot Studio. More integrations are coming - this is just the beginning.

## What You'll Build

By the end of this tutorial, you'll have:
1. A working MCP server running locally
2. The server containerized and ready to deploy
3. The server live on Azure Container Apps
4. Integration with Microsoft Copilot Studio for testing

## Prerequisites

You'll need:
- **Python 3.11+** (3.11 recommended - check the Dockerfile if you want specifics)
- **UV** package manager (we'll install this)
- **Podman** for containerization (Docker works too, just swap the commands)
- **VS Code** (optional, but useful for port forwarding)
- **Azure subscription** for deployment
- **Microsoft Copilot Studio** access for testing

## Repository Contents

```
.
├── server.py              # Your MCP server code
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container definition
├── docker-compose.yml    # Podman/Docker compose configuration
└── README.md            # This file
```

---

## Part 1: Build and Run Locally

### Step 1: Install UV

UV is a fast Python package manager. Get it installed first.

**macOS or Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows PowerShell:**
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

**Verify installation:**
```bash
uv --version
```

### Step 2: Set Up Your Project

```bash
mkdir joke-mcp
cd joke-mcp
```

### Step 3: Install Python with UV

**List available versions:**
```bash
uv python list
```

**Install Python 3.11:**
```bash
uv python install 3.11
```

### Step 4: Create a Virtual Environment

```bash
uv venv .venv --python 3.11
```

**Activate it:**

*macOS or Linux:*
```bash
source .venv/bin/activate
```

*Windows PowerShell:*
```powershell
.venv\Scripts\Activate.ps1
```

**Confirm it worked:**
```bash
python --version
which python   # macOS or Linux
where python   # Windows
```

### Step 5: Add Your Server Code

Create `server.py` with your MCP server implementation. The key part is the HTTP transport configuration:

```python
# At the bottom of your server.py
if __name__ == "__main__":
    import sys
    print("Starting Joke MCP Server with HTTP transport on http://localhost:2009/mcp", file=sys.stderr)
    mcp.run(transport="http", host="0.0.0.0", port=2009, path="/mcp")
```

### Step 6: Install Dependencies

```bash
uv add mcp
```

This creates `uv.lock` and installs everything into your virtual environment.

### Step 7: Run the Server

```bash
uv run python server.py
```

You should see the startup message about HTTP on localhost:2009. If you see a stack trace instead, the server is upset. Check your code.

### Step 8: Quick Sanity Check

Open another terminal and test the endpoint:

```bash
curl -i http://localhost:2009/mcp
```

You won't get a pretty page. This is an MCP endpoint - silence or a structured response is normal.

---

## Part 2: Test with Microsoft Copilot Studio

### Option A: Direct Local Testing (Quick)

If you're running everything on the same machine, just point Claude or VS-Code or MCP capable agents to:
```
http://localhost:2009/mcp
```

### Option B: Remote Testing with VS Code Port Forwarding (Better)

If your server is running on a remote machine, dev container, or you want a public URL:

1. **Run your server** in the remote environment
2. **Open VS Code** - the Ports panel should auto-detect port 2009
3. **Forward the port** - click "Forward Port" in the Ports panel
4. **Make it public** if you want a shareable URL
5. **Copy the forwarded URL** (e.g., `https://xyz.devtunnels.ms`)

<!-- Screenshot suggestion: VS Code Ports panel with forwarded port highlighted -->

### Connect to Copilot Studio

1. Open or create your agent in **Microsoft Copilot Studio**
2. Go to **Tools** → **Add a tool** → **+ New tool**
3. Select **Model Context Protocol**
4. Configure:
   - **Name**: Something clear like `joke-mcp-local-test`
   - **Description**: Be specific - this helps the agent understand when to use your tool
   - **Endpoint URL**: Your forwarded URL + `/mcp` (e.g., `https://xyz.devtunnels.ms/mcp`)
   - **Authentication**: None (for now - see note below)
5. Click **Create**

<!-- Screenshot suggestion: MCP tool configuration dialog in Copilot Studio -->

6. **Check connections** in Connection Manager one more time
7. **Test in the test pane**

<!-- Screenshot suggestion: Successful test conversation showing MCP server responding -->

**Authentication Note:**  
This example skips authentication to keep things simple. For production, **you absolutely should add authentication**. I'll probably write a V2 of this tutorial with proper auth implementation. Until then, don't expose unauthenticated servers to the internet.

### Common Local Testing Issues

| Problem | Fix |
|---------|-----|
| Port already in use | Change the port in `server.py`, or kill whatever's using 2009 |
| Package not found | Make sure you ran `uv add mcp` with the correct package name |
| Windows firewall prompt | Allow local access, unless you enjoy debugging networking |
| Connection refused in Copilot Studio | Check your port forwarding and make sure the `/mcp` path is included |

---

## Part 3: Containerize with Podman

### Step 1: Create Your Container Files

You need three files (check this repo for examples):

1. **server.py** - Your MCP server code
2. **requirements.txt** - Your Python dependencies
3. **Dockerfile** - Container build instructions
4. **docker-compose.yml** - Compose configuration

### Step 2: Build the Container

Navigate to your project folder:

```bash
cd joke-mcp
```

Build with Podman:
```bash
podman-compose build
```

### Step 3: Run Locally

```bash
podman-compose up
```

The server should start inside the container. Test it the same way as before.

---

## Part 4: Multi-Architecture Build and Push to Docker Hub

If you want to support both Intel/AMD (amd64) and ARM (arm64) processors, build a multi-architecture image.

### Step 1: Build Per-Architecture Images

```bash
podman build --platform=linux/amd64 -t localhost/jokes-mcp_joke-mcp:amd64 .
podman build --platform=linux/arm64 -t localhost/jokes-mcp_joke-mcp:arm64 .
```

### Step 2: Tag for Docker Hub

Replace `roelzz/jokes-mcp_joke-mcp` with your Docker Hub username and repo:

```bash
podman tag localhost/jokes-mcp_joke-mcp:amd64 docker.io/roelzz/jokes-mcp_joke-mcp:amd64
podman tag localhost/jokes-mcp_joke-mcp:arm64 docker.io/roelzz/jokes-mcp_joke-mcp:arm64
```

### Step 3: Login to Docker Hub

```bash
podman login docker.io
```

### Step 4: Push Each Architecture

```bash
podman push docker.io/roelzz/jokes-mcp_joke-mcp:amd64
podman push docker.io/roelzz/jokes-mcp_joke-mcp:arm64
```

### Step 5: Create a Manifest List

This groups both images under one tag:

```bash
podman manifest create docker.io/roelzz/jokes-mcp_joke-mcp:latest
podman manifest add docker.io/roelzz/jokes-mcp_joke-mcp:latest docker.io/roelzz/jokes-mcp_joke-mcp:amd64
podman manifest add docker.io/roelzz/jokes-mcp_joke-mcp:latest docker.io/roelzz/jokes-mcp_joke-mcp:arm64
```

### Step 6: Push the Manifest

```bash
podman manifest push docker.io/roelzz/jokes-mcp_joke-mcp:latest
```

Now anyone can run:
```bash
docker pull roelzz/jokes-mcp_joke-mcp:latest
```

Docker/Podman automatically pulls the right architecture for their CPU.

---

## Part 5: Deploy to Azure Container Apps

### Step 1: Go to Azure Portal

1. Navigate to [portal.azure.com](https://portal.azure.com)
2. Click **Create a resource**
3. Search for and select **Container App**

<!-- Screenshot suggestion: Azure Portal Container App creation page -->

### Step 2: Configure the Container App

1. **Basics:**
   - Select your subscription
   - Choose or create a resource group
   - Pick a region (close to your users)
   - Give it a name

2. **Container:**
   - **Deployment source**: Container Image
   - **Image source**: Docker Hub (or your registry)
   - **Registry**: docker.io
   - **Image and tag**: `roelzz/jokes-mcp_joke-mcp:latest` (use your path)

3. **Ingress:**
   - Enable ingress
   - Set target port to `2009`
   - Enable external traffic

4. Review and create

### Step 3: Get Your Public URL

Once deployed:
1. Go to your Container App in the Azure Portal
2. Find the **Application URL** in the overview
3. Your MCP endpoint is: `https://your-app-url.azurecontainerapps.io/mcp`

<!-- Screenshot suggestion: Azure Container App overview showing Application URL -->

### Step 4: Update Copilot Studio

Go back to your MCP tool configuration in Copilot Studio and update the endpoint URL to your new Azure URL (don't forget the `/mcp` at the end).

Test again. If it works, congratulations - you just deployed your first MCP server to production.

---

## Troubleshooting

### Common Issues

**Server won't start locally:**
- Check Python version matches requirements
- Verify all dependencies installed with `uv add`
- Look for typos in `server.py`

**Container build fails:**
- Check Dockerfile syntax
- Ensure requirements.txt is complete
- Verify base image is accessible

**Azure deployment issues:**
- Confirm image pushed to registry successfully
- Check ingress settings (port 2009, external enabled)
- Review container logs in Azure Portal

**Copilot Studio can't connect:**
- Verify endpoint URL includes `/mcp` path
- Check server is actually running
- Test endpoint with curl first
- For Azure: ensure ingress allows external traffic

*More troubleshooting tips will be added as common issues emerge.*

---

## What's Next?

This is Version 1 - functional but basic. Future improvements:

- **V2: Authentication** - Add proper API key or OAuth implementation
- **Advanced MCP features** - More complex tools and resources
- **Monitoring** - Add logging and health checks
- **CI/CD** - Automated build and deployment pipeline

## Future MCP Support

Microsoft Copilot Studio currently supports MCP servers, and more AI platforms will likely add support in the future. The protocol is designed to be platform-agnostic, so your server should work with other tools as they adopt MCP.

---

## Contributing

Go nuts. Fork this repo, modify it, break it, fix it, make it better. If you have improvements or find issues, reach out or submit a pull request. The goal is to help people build MCP servers without the headache.

---

## License

This project is licensed under the MIT License - which means you can do whatever you want with it. Use it, modify it, sell it, teach with it. Just don't blame me if something breaks.

---

## Author

Check out my other projects on [GitHub](https://github.com/roelzz)

---

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Microsoft Copilot Studio Documentation](https://learn.microsoft.com/en-us/microsoft-copilot-studio/)
- [UV Package Manager](https://github.com/astral-sh/uv)
- [Podman Documentation](https://podman.io/)
- [Azure Container Apps Documentation](https://learn.microsoft.com/en-us/azure/container-apps/)

---

**Built with no patience for complexity. If it's not working, it's probably simpler than you think.**
