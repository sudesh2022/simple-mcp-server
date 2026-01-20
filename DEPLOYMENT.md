# Deployment Guide for Render.com

This guide will walk you through deploying your MCP server to Render.com.

## Prerequisites

- A GitHub account
- A Render.com account (free tier available)
- Git installed on your local machine

## Step-by-Step Deployment

### 1. Initialize Git Repository

If you haven't already, initialize a git repository in your project folder:

```bash
cd /Users/sudeshkrishnamoorthy/Documents/IBM/2026/publicmcpserver
git init
git add .
git commit -m "Initial commit: Simple MCP Server"
```

### 2. Create GitHub Repository

1. Go to [GitHub](https://github.com) and log in
2. Click the "+" icon in the top right and select "New repository"
3. Name your repository (e.g., `simple-mcp-server`)
4. Choose "Public" or "Private" (both work with Render)
5. Do NOT initialize with README (we already have files)
6. Click "Create repository"

### 3. Push to GitHub

Copy the commands from GitHub's "push an existing repository" section:

```bash
git remote add origin https://github.com/YOUR_USERNAME/simple-mcp-server.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### 4. Deploy on Render.com

1. **Sign up/Login to Render**
   - Go to [Render.com](https://render.com)
   - Sign up for a free account or log in

2. **Create New Web Service**
   - Click "New +" button in the top right
   - Select "Blueprint" from the dropdown
   
3. **Connect GitHub Repository**
   - If this is your first time, you'll need to connect your GitHub account
   - Click "Connect GitHub" and authorize Render
   - Select your `simple-mcp-server` repository

4. **Configure Blueprint**
   - Render will automatically detect the `render.yaml` file
   - Review the configuration:
     - **Name**: simple-mcp-server
     - **Environment**: Python
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 mcp_sse_server:app`
   - Click "Apply" to deploy
   
   **Note**: This deploys the MCP SSE server (proper MCP protocol). To deploy the simple REST API instead, change the start command to `gunicorn http_server:app`

5. **Wait for Deployment**
   - Render will start building your application
   - This usually takes 2-5 minutes
   - You can watch the build logs in real-time

6. **Access Your Server**
   - Once deployed, Render will provide a URL like:
     `https://simple-mcp-server-xxxx.onrender.com`
   - Click the URL to test your server

## Testing Your Deployed Server

### Using a Web Browser

Simply visit your Render URL to see the server information:
```
https://your-app-name.onrender.com/
```

### Using curl (MCP SSE Protocol)

```bash
# Get server info
curl https://your-app-name.onrender.com/

# Health check
curl https://your-app-name.onrender.com/health

# List available tools
curl -X POST https://your-app-name.onrender.com/sse \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# Echo test
curl -X POST https://your-app-name.onrender.com/sse \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"echo","arguments":{"text":"Hello from Render!"}}}'

# Calculate
curl -X POST https://your-app-name.onrender.com/sse \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"calculate","arguments":{"operation":"add","a":10,"b":5}}}'

# Get current time
curl -X POST https://your-app-name.onrender.com/sse \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"get_current_time","arguments":{}}}'

# Reverse text
curl -X POST https://your-app-name.onrender.com/sse \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"reverse_text","arguments":{"text":"Render.com"}}}'
```

**For detailed testing instructions, see [SSE_TESTING.md](SSE_TESTING.md)**

### Using Python (MCP Client)

```python
import requests
import json

BASE_URL = "https://your-app-name.onrender.com/sse"

def call_mcp_tool(tool_name, arguments):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    response = requests.post(BASE_URL, json=payload)
    
    # Parse SSE response
    for line in response.text.split('\n'):
        if line.startswith('data: '):
            data = json.loads(line[6:])
            return data

# Echo
result = call_mcp_tool("echo", {"text": "Hello, World!"})
print(result)

# Calculate
result = call_mcp_tool("calculate", {"operation": "multiply", "a": 7, "b": 6})
print(result)
```

### Using with Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on Mac):

```json
{
  "mcpServers": {
    "simple-mcp-server": {
      "url": "https://your-app-name.onrender.com/sse",
      "transport": "sse"
    }
  }
}
```

## Updating Your Deployment

Whenever you make changes to your code:

```bash
git add .
git commit -m "Description of your changes"
git push
```

Render will automatically detect the changes and redeploy your application!

## Monitoring and Logs

1. Go to your Render dashboard
2. Click on your service name
3. Navigate to the "Logs" tab to see real-time logs
4. Check the "Metrics" tab for performance data

## Free Tier Limitations

Render's free tier includes:
- ✅ 750 hours of runtime per month
- ✅ Automatic HTTPS
- ✅ Automatic deploys from Git
- ⚠️ Services spin down after 15 minutes of inactivity
- ⚠️ First request after spin-down may take 30-60 seconds

To keep your service always active, upgrade to a paid plan ($7/month).

## Troubleshooting

### Build Failed
- Check the build logs in Render dashboard
- Ensure `requirements.txt` is correct
- Verify Python version compatibility

### Service Won't Start
- Check the logs for error messages
- Ensure `http_server.py` has no syntax errors
- Verify the start command in `render.yaml`

### 502 Bad Gateway
- Service might be starting up (wait 30-60 seconds)
- Check if the service is running in the Render dashboard

## Environment Variables (Optional)

If you need to add environment variables:

1. Go to your service in Render dashboard
2. Click "Environment" tab
3. Add key-value pairs
4. Click "Save Changes"

The service will automatically redeploy.

## Custom Domain (Optional)

To use a custom domain:

1. Go to your service settings
2. Click "Custom Domains"
3. Add your domain
4. Update your DNS records as instructed

## Next Steps

- Add more tools to your MCP server
- Implement authentication for sensitive operations
- Add rate limiting
- Set up monitoring and alerts
- Create a frontend UI for your server

## Support

- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com)
- [MCP Documentation](https://modelcontextprotocol.io)

---

**Congratulations!** 🎉 Your MCP server is now live on the internet!
