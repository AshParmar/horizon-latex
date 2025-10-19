# 🔑 API Keys Setup Guide

## For Local Development

Your API keys should go in the `.env` file in the root directory. This file is already configured with your working credentials.

### Current Setup (Ready to Use):

The `.env` file already contains your working API keys:

```bash
COMPOSIO_API_KEY=jbjbjbjkjbjb
GMAIL_USER_ID=ufhfjfjfjfj
GROQ_API_KEY=kbkbkk
# ... and all other credentials
```

### Test Your Setup:

```bash
# Activate virtual environment
.\comp\Scripts\Activate.ps1

# Test configuration
python -c "from minimal_config import validate_config; validate_config()"

# Test Gmail monitor
python auto_gmail_monitor.py

# Test full pipeline
python ultimate_ai_recruiter_pipeline.py
```

### Security Notes:

1. ✅ **`.env` file is in `.gitignore`** - Won't be committed to GitHub
2. ✅ **All credentials loaded from environment variables** - No hardcoded keys in code
3. ✅ **`.env.example` template provided** - For other developers to copy

### For New Users:

If someone else wants to use this project:

1. Copy `.env.example` to `.env`
2. Replace placeholder values with their own API keys
3. Get credentials from:
   - **Composio**: https://app.composio.dev/settings
   - **Groq**: https://console.groq.com/keys
   - **Gmail/LinkedIn/Sheets**: Connect in Composio Dashboard

### File Structure:

```
📁 Project Root
├── .env                 # ← Your REAL API keys go here (LOCAL ONLY)
├── .env.example         # ← Template for others
├── .env.local.example   # ← Your working values (for reference)
├── minimal_config.py    # ← Loads from .env
└── .gitignore          # ← Protects .env from being committed
```

## 🚀 You're All Set!

Your local environment is ready to run with all the working API keys configured securely.