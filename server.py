#!/usr/bin/env python3
"""
Simple MCP Server with basic tools
This server provides basic utilities like echo, time, and calculations
"""

import asyncio
import json
import sys
from datetime import datetime
from typing import Any

from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
import mcp.server.stdio


# Create server instance
server = Server("simple-mcp-server")


@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources"""
    return [
        Resource(
            uri="resource://server-info",
            name="Server Information",
            mimeType="text/plain",
            description="Information about this MCP server"
        )
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource by URI"""
    if uri == "resource://server-info":
        return """Simple MCP Server
        
This is a basic MCP server that provides utility tools:
- Echo: Returns the input text
- Current Time: Returns the current server time
- Calculate: Performs basic arithmetic operations
- Reverse Text: Reverses the input text

Version: 1.0.0
"""
    else:
        raise ValueError(f"Unknown resource: {uri}")


@server.list_tools()
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


@server.call_tool()
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


async def main():
    """Main entry point"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
