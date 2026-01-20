# Quick Start Guide

Get your MCP server running in 5 minutes!

## Local Testing (Right Now!)

### 1. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python http_server.py
```

The server will start at `http://localhost:8000`

### 3. Test It
Open a new terminal and run:
```bash
python test_server.py
```

Or visit `http://localhost:8000` in your browser!

## Deploy to Render.com (5 Minutes!)

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Deploy on Render
1. Go to [render.com](https://render.com)
2. Click "New +" → "Blueprint"
3. Connect your GitHub repo
4. Click "Apply"

### 3. Done! 🎉
Your server will be live at `https://your-app.onrender.com`

## Quick API Examples

### Echo
```bash
curl -X POST https://your-app.onrender.com/tools/echo \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello!"}'
```

### Calculate
```bash
curl -X POST https://your-app.onrender.com/tools/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "multiply", "a": 7, "b": 6}'
```

### Get Time
```bash
curl https://your-app.onrender.com/tools/time
```

### Reverse Text
```bash
curl -X POST https://your-app.onrender.com/tools/reverse \
  -H "Content-Type: application/json" \
  -d '{"text": "MCP"}'
```

## What's Included?

- ✅ **server.py** - Standard MCP server (stdio)
- ✅ **http_server.py** - HTTP wrapper for web deployment
- ✅ **test_server.py** - Comprehensive test suite
- ✅ **render.yaml** - Render.com deployment config
- ✅ **README.md** - Full documentation
- ✅ **DEPLOYMENT.md** - Detailed deployment guide

## Need Help?

- 📖 Read the full [README.md](README.md)
- 🚀 Check the [DEPLOYMENT.md](DEPLOYMENT.md) guide
- 🧪 Run `python test_server.py` to verify everything works

## Next Steps

1. Customize the tools in `http_server.py`
2. Add authentication if needed
3. Connect to a database
4. Build a frontend UI
5. Add more MCP tools!

---

**Happy coding!** 🚀
