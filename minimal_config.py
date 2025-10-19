"""
Minimal Configuration for Composio + Groq Enrichment
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# LinkedIn Integration
LINKEDIN_CONNECTED_ACCOUNT_ID = os.getenv("LINKEDIN_CONNECTED_ACCOUNT_ID", "")
LINKEDIN_ENTITY_ID = os.getenv("LINKEDIN_ENTITY_ID", "")

# User ID for Composio (must be UUID format)
USER_ID = os.getenv("LINKEDIN_ENTITY_ID", "pg-test-82fe45fd-72dd-4266-8d24-61c90d1c01be")

# Gmail Integration Credentials
GMAIL_ACCOUNT_ID = "ca_T1yVWb6wbXsD"
GMAIL_USER_ID = "pg-test-82fe45fd-72dd-4266-8d24-61c90d1c01be"
GMAIL_AUTH_CONFIG_ID = "ac_YT-t3VYqgxGU"

# Google Sheets Integration
GOOGLE_SHEETS_AUTH_CONFIG_ID = "ac_R98zJIL-7OuB"
GOOGLE_SHEETS_ACCOUNT_ID = "ca_90gZQ-91AShF"
GOOGLE_SHEETS_USER_ID = "pg-test-82fe45fd-72dd-4266-8d24-61c90d1c01be"

# LLM Settings  
GROQ_MODEL = "llama-3.1-8b-instant"  # Reliable primary model
GROQ_MODEL_BACKUP = "llama-3.1-70b-versatile"  # Backup model
GROQ_MODEL_ALTERNATIVE = "meta-llama/llama-4-scout-17b-16e-instruct"  # Alternative for specific tasks