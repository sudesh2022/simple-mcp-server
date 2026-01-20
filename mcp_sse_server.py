#!/usr/bin/env python3
"""
MCP SSE Server - Proper MCP protocol implementation with SSE transport
This server is compatible with MCP gateways and clients
"""

from flask import Flask, request, Response
from datetime import datetime
import json
import asyncio
from typing import Any

from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
)

app = Flask(__name__)

# Create MCP server instance
mcp_server = Server("simple-mcp-server")


@mcp_server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="echo",
            description="Echoes back the input text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to echo back"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="get_current_time",
            description="Returns the current server time",
            inputSchema={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone (optional, defaults to UTC)",
                        "default": "UTC"
                    }
                }
            }
        ),
        Tool(
            name="calculate",
            description="Performs basic arithmetic operations",
            inputSchema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "The operation to perform"
                    },
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["operation", "a", "b"]
            }
        ),
        Tool(
            name="reverse_text",
            description="Reverses the input text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to reverse"
                    }
                },
                "required": ["text"]
            }
        )
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "echo":
        text = arguments.get("text", "")
        return [TextContent(type="text", text=f"Echo: {text}")]
    
    elif name == "get_current_time":
        current_time = datetime.now().isoformat()
        return [TextContent(
            type="text",
            text=f"Current server time: {current_time}"
        )]
    
    elif name == "calculate":
        operation = arguments.get("operation")
        a = arguments.get("a")
        b = arguments.get("b")
        
        try:
            if operation == "add":
                result = a + b
            elif operation == "subtract":
                result = a - b
            elif operation == "multiply":
                result = a * b
            elif operation == "divide":
                if b == 0:
                    return [TextContent(type="text", text="Error: Division by zero")]
                result = a / b
            else:
                return [TextContent(type="text", text=f"Unknown operation: {operation}")]
            
            return [TextContent(
                type="text",
                text=f"Result: {a} {operation} {b} = {result}"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif name == "reverse_text":
        text = arguments.get("text", "")
        reversed_text = text[::-1]
        return [TextContent(
            type="text",
            text=f"Reversed: {reversed_text}"
        )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


@app.route('/sse', methods=['GET', 'POST'])
def sse_endpoint():
    """SSE endpoint for MCP protocol"""
    
    def generate():
        """Generate SSE events"""
        try:
            if request.method == 'POST':
                # Handle MCP request
                data = request.get_json()
                
                # Process based on method
                method = data.get('method', '')
                
                if method == 'tools/list':
                    # List tools
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    tools = loop.run_until_complete(list_tools())
                    loop.close()
                    
                    response = {
                        "jsonrpc": "2.0",
                        "id": data.get('id'),
                        "result": {
                            "tools": [
                                {
                                    "name": tool.name,
                                    "description": tool.description,
                                    "inputSchema": tool.inputSchema
                                }
                                for tool in tools
                            ]
                        }
                    }
                    yield f"data: {json.dumps(response)}\n\n"
                
                elif method == 'tools/call':
                    # Call tool
                    params = data.get('params', {})
                    tool_name = params.get('name')
                    arguments = params.get('arguments', {})
                    
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    result = loop.run_until_complete(call_tool(tool_name, arguments))
                    loop.close()
                    
                    response = {
                        "jsonrpc": "2.0",
                        "id": data.get('id'),
                        "result": {
                            "content": [
                                {
                                    "type": content.type,
                                    "text": content.text
                                }
                                for content in result
                            ]
                        }
                    }
                    yield f"data: {json.dumps(response)}\n\n"
                
                else:
                    # Unknown method
                    response = {
                        "jsonrpc": "2.0",
                        "id": data.get('id'),
                        "error": {
                            "code": -32601,
                            "message": f"Method not found: {method}"
                        }
                    }
                    yield f"data: {json.dumps(response)}\n\n"
            
            else:
                # GET request - send server info
                info = {
                    "jsonrpc": "2.0",
                    "method": "server/info",
                    "params": {
                        "name": "simple-mcp-server",
                        "version": "1.0.0",
                        "description": "A basic MCP server with utility tools"
                    }
                }
                yield f"data: {json.dumps(info)}\n\n"
        
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
            yield f"data: {json.dumps(error_response)}\n\n"
    
    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive'
        }
    )


@app.route('/')
def home():
    """Home endpoint with server information"""
    return {
        "name": "Simple MCP Server",
        "version": "1.0.0",
        "description": "A basic MCP server with utility tools",
        "protocol": "MCP with SSE transport",
        "endpoints": {
            "/": "Server information",
            "/sse": "MCP SSE endpoint (GET for info, POST for requests)"
        }
    }


@app.route('/health')
def health():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, threaded=True)
