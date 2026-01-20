#!/usr/bin/env python3
"""
HTTP wrapper for MCP Server
This allows the MCP server to be accessed via HTTP endpoints
"""

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def home():
    """Home endpoint with server information"""
    return jsonify({
        "name": "Simple MCP Server",
        "version": "1.0.0",
        "description": "A basic MCP server with utility tools",
        "endpoints": {
            "/": "Server information",
            "/health": "Health check",
            "/tools": "List available tools",
            "/tools/echo": "Echo tool",
            "/tools/time": "Current time tool",
            "/tools/calculate": "Calculator tool",
            "/tools/reverse": "Text reversal tool"
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


@app.route('/tools')
def list_tools():
    """List all available tools"""
    return jsonify({
        "tools": [
            {
                "name": "echo",
                "description": "Echoes back the input text",
                "endpoint": "/tools/echo",
                "method": "POST",
                "parameters": {
                    "text": "string (required)"
                }
            },
            {
                "name": "get_current_time",
                "description": "Returns the current server time",
                "endpoint": "/tools/time",
                "method": "GET"
            },
            {
                "name": "calculate",
                "description": "Performs basic arithmetic operations",
                "endpoint": "/tools/calculate",
                "method": "POST",
                "parameters": {
                    "operation": "string (required): add, subtract, multiply, divide",
                    "a": "number (required)",
                    "b": "number (required)"
                }
            },
            {
                "name": "reverse_text",
                "description": "Reverses the input text",
                "endpoint": "/tools/reverse",
                "method": "POST",
                "parameters": {
                    "text": "string (required)"
                }
            }
        ]
    })


@app.route('/tools/echo', methods=['POST'])
def echo():
    """Echo tool endpoint"""
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' parameter"}), 400
    
    return jsonify({
        "tool": "echo",
        "result": f"Echo: {data['text']}"
    })


@app.route('/tools/time', methods=['GET'])
def get_time():
    """Current time tool endpoint"""
    return jsonify({
        "tool": "get_current_time",
        "result": datetime.now().isoformat(),
        "timezone": "UTC"
    })


@app.route('/tools/calculate', methods=['POST'])
def calculate():
    """Calculator tool endpoint"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Missing request body"}), 400
    
    operation = data.get('operation')
    a = data.get('a')
    b = data.get('b')
    
    if not all([operation, a is not None, b is not None]):
        return jsonify({"error": "Missing required parameters: operation, a, b"}), 400
    
    try:
        a = float(a)
        b = float(b)
        
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                return jsonify({"error": "Division by zero"}), 400
            result = a / b
        else:
            return jsonify({"error": f"Unknown operation: {operation}"}), 400
        
        return jsonify({
            "tool": "calculate",
            "operation": operation,
            "a": a,
            "b": b,
            "result": result
        })
    except ValueError as e:
        return jsonify({"error": f"Invalid number format: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tools/reverse', methods=['POST'])
def reverse_text():
    """Text reversal tool endpoint"""
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' parameter"}), 400
    
    text = data['text']
    reversed_text = text[::-1]
    
    return jsonify({
        "tool": "reverse_text",
        "original": text,
        "result": reversed_text
    })


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
