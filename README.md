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

This project includes two versions of the server:

1. **`server.py`** - Standard MCP server using stdio (for local use with MCP clients)
2. **`http_server.py`** - HTTP wrapper version (for web deployment to Render.com)

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
   - Use the API endpoints to interact with the tools

### API Endpoints

Once deployed, you can access these endpoints:

- `GET /` - Server information and available endpoints
- `GET /health` - Health check
- `GET /tools` - List all available tools
- `POST /tools/echo` - Echo tool
  ```json
  {"text": "Hello, World!"}
  ```
- `GET /tools/time` - Get current server time
- `POST /tools/calculate` - Calculator
  ```json
  {"operation": "add", "a": 5, "b": 3}
  ```
- `POST /tools/reverse` - Reverse text
  ```json
  {"text": "Hello"}
  ```

### Testing the Deployed Server

Using curl:
```bash
# Get server info
curl https://your-app.onrender.com/

# Echo test
curl -X POST https://your-app.onrender.com/tools/echo \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, MCP!"}'

# Calculate
curl -X POST https://your-app.onrender.com/tools/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "multiply", "a": 7, "b": 6}'

# Get current time
curl https://your-app.onrender.com/tools/time

# Reverse text
curl -X POST https://your-app.onrender.com/tools/reverse \
  -H "Content-Type: application/json" \
  -d '{"text": "MCP Server"}'
```

## Advanced: HTTP Wrapper (Optional)

The HTTP wrapper (`http_server.py`) is already included and configured for Render.com deployment. It provides a REST API interface to the MCP server functionality, making it accessible via standard HTTP requests.

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
