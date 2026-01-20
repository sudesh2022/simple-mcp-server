# Testing the MCP SSE Server

This guide explains how to test your deployed MCP SSE server on Render.com.

## What is the SSE Endpoint?

Your MCP server uses **Server-Sent Events (SSE)** to implement the MCP protocol over HTTP. The main endpoint is:

```
https://your-app.onrender.com/sse
```

## Available Endpoints

### 1. Root Endpoint - Server Info
```bash
curl https://your-app.onrender.com/
```

**Response:**
```json
{
  "name": "Simple MCP Server",
  "version": "1.0.0",
  "description": "A basic MCP server with utility tools",
  "protocol": "MCP with SSE transport",
  "endpoints": {
    "/": "Server information",
    "/sse": "MCP SSE endpoint (GET for info, POST for requests)"
  }
}
```

### 2. Health Check
```bash
curl https://your-app.onrender.com/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-20T06:52:00.000Z"
}
```

### 3. SSE Endpoint - Server Info (GET)
```bash
curl https://your-app.onrender.com/sse
```

**Response:** (SSE stream)
```
data: {"jsonrpc":"2.0","method":"server/info","params":{"name":"simple-mcp-server","version":"1.0.0","description":"A basic MCP server with utility tools"}}
```

## Testing MCP Protocol via SSE

### List Available Tools

```bash
curl -X POST https://your-app.onrender.com/sse \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list"
  }'
```

**Response:**
```
data: {"jsonrpc":"2.0","id":1,"result":{"tools":[{"name":"echo","description":"Echoes back the input text","inputSchema":{...}},...]}}
```

### Call the Echo Tool

```bash
curl -X POST https://your-app.onrender.com/sse \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "echo",
      "arguments": {
        "text": "Hello from SSE!"
      }
    }
  }'
```

**Response:**
```
data: {"jsonrpc":"2.0","id":2,"result":{"content":[{"type":"text","text":"Echo: Hello from SSE!"}]}}
```

### Call the Calculate Tool

```bash
curl -X POST https://your-app.onrender.com/sse \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "calculate",
      "arguments": {
        "operation": "multiply",
        "a": 7,
        "b": 6
      }
    }
  }'
```

**Response:**
```
data: {"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"Result: 7 multiply 6 = 42"}]}}
```

### Call the Get Current Time Tool

```bash
curl -X POST https://your-app.onrender.com/sse \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 4,
    "method": "tools/call",
    "params": {
      "name": "get_current_time",
      "arguments": {}
    }
  }'
```

### Call the Reverse Text Tool

```bash
curl -X POST https://your-app.onrender.com/sse \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 5,
    "method": "tools/call",
    "params": {
      "name": "reverse_text",
      "arguments": {
        "text": "MCP Server"
      }
    }
  }'
```

## Using with MCP Clients

### Claude Desktop Configuration

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on Mac):

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

### Python MCP Client

```python
import requests
import json

BASE_URL = "https://your-app.onrender.com/sse"

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

# Example usage
result = call_mcp_tool("echo", {"text": "Hello!"})
print(result)
```

## Understanding SSE Responses

SSE responses are formatted as:
```
data: <JSON payload>

```

Each line starting with `data:` contains a JSON-RPC message. The double newline indicates the end of an event.

## Troubleshooting

### Connection Issues
- **502 Bad Gateway**: Service is starting up (wait 30-60 seconds on free tier)
- **Timeout**: Increase timeout in your client (SSE connections are long-lived)

### Invalid Responses
- Ensure you're sending proper JSON-RPC 2.0 format
- Check that `method` is one of: `tools/list`, `tools/call`
- Verify tool names match exactly: `echo`, `get_current_time`, `calculate`, `reverse_text`

### Testing Tips
1. Always test `/health` endpoint first to ensure server is running
2. Use `tools/list` to verify available tools
3. Check request/response IDs match in JSON-RPC
4. SSE responses include `data:` prefix - strip it when parsing JSON

## Next Steps

- Connect from Claude Desktop or other MCP clients
- Monitor logs in Render dashboard
- Add authentication for production use
- Implement rate limiting
- Add custom tools to extend functionality