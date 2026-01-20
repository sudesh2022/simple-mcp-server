# Simple Python MCP Server

A basic Model Context Protocol (MCP) server written in Python that provides utility tools.

## Features

This MCP server provides the following tools:

1. **Echo** - Echoes back the input text
2. **Get Current Time** - Returns the current server time
3. **Calculate** - Performs basic arithmetic operations (add, subtract, multiply, divide)
4. **Reverse Text** - Reverses the input text

## Local Development

### Prerequisites

- Python 3.10 or higher
- pip

### Setup

1. Clone this repository or download the files

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python server.py
```

## Testing Locally

You can test the server using the MCP Inspector or by configuring it in your MCP client.

### Using MCP Inspector

```bash
npx @modelcontextprotocol/inspector python server.py
```

## Deploying to Render.com

This project includes three versions of the server:

1. **`server.py`** - Standard MCP server using stdio (for local use with MCP clients)
2. **`http_server.py`** - HTTP REST API wrapper (simple REST endpoints)
3. **`mcp_sse_server.py`** - MCP server with SSE transport (proper MCP protocol over HTTP) ⭐ **Deployed Version**

### Quick Deploy to Render.com

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to [Render.com](https://render.com) and sign up/login
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will detect `render.yaml` automatically
   - Click "Apply" to deploy

3. **Access Your Server**:
   - Once deployed, Render will provide a URL (e.g., `https://simple-mcp-server.onrender.com`)
   - Visit the URL to see server information
   - Use the MCP SSE endpoint to interact with the tools

### MCP SSE Endpoints

The deployed server uses **Server-Sent Events (SSE)** to implement the MCP protocol over HTTP:

- `GET /` - Server information and available endpoints
- `GET /health` - Health check
- `GET /sse` - SSE endpoint (server info stream)
- `POST /sse` - MCP protocol endpoint (JSON-RPC 2.0)

### Testing the Deployed Server

**Basic Health Check:**
```bash
# Get server info
curl https://your-app.onrender.com/

# Health check
curl https://your-app.onrender.com/health
```

**MCP Protocol Testing:**
```bash
# List available tools
curl -X POST https://your-app.onrender.com/sse \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# Call echo tool
curl -X POST https://your-app.onrender.com/sse \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"echo","arguments":{"text":"Hello MCP!"}}}'

# Call calculate tool
curl -X POST https://your-app.onrender.com/sse \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"calculate","arguments":{"operation":"multiply","a":7,"b":6}}}'
```

**For detailed testing instructions, see [SSE_TESTING.md](SSE_TESTING.md)**

## Using with MCP Clients

### Claude Desktop Configuration

Add to your Claude Desktop config:
```json
{
  "mcpServers": {
    "simple-mcp-server": {
      "url": "https://your-app.onrender.com/sse",
      "transport": "sse"
    }
  }
}
```

## Alternative: HTTP REST API

If you prefer a simple REST API instead of MCP protocol, you can deploy `http_server.py` instead:
1. Change `render.yaml` startCommand to: `gunicorn http_server:app`
2. Redeploy
3. Use standard REST endpoints (see `http_server.py` for details)

## Configuration

The server runs on stdio by default. No additional configuration is needed for basic usage.

## Resources

The server provides one resource:
- `resource://server-info` - Information about the server and its capabilities

## Tools

### echo
Echoes back the input text.

**Parameters:**
- `text` (string, required): The text to echo

### get_current_time
Returns the current server time in ISO format.

**Parameters:**
- `timezone` (string, optional): Timezone (defaults to UTC)

### calculate
Performs basic arithmetic operations.

**Parameters:**
- `operation` (string, required): One of "add", "subtract", "multiply", "divide"
- `a` (number, required): First number
- `b` (number, required): Second number

### reverse_text
Reverses the input text.

**Parameters:**
- `text` (string, required): The text to reverse

## License

MIT

## Contributing

Feel free to submit issues and enhancement requests!
