# 🚀 AI Recruiter Copilot - Complete Pipeline

## Overview
Advanced candidate enrichment system using LinkedIn API, LLM processing, and automated Google Sheets export for recruiters.

## 🎯 Features
- **LinkedIn Integration**: Real profile data via Composio API
- **AI Enhancement**: Groq LLM for candidate summaries and skills extraction  
- **Google Sheets Export**: Automated spreadsheet creation and population
- **CSV Fallback**: Reliable data export for any platform
- **Complete Pipeline**: End-to-end candidate processing

## 📁 Core Files

### 🔧 Configuration
- `minimal_config.py` - API keys and settings
- `requirements_minimal.txt` - Python dependencies
- `.env` - Environment variables (API keys)

### 🤖 Core Modules
- `minimal_models.py` - Pydantic data models
- `minimal_linkedin.py` - LinkedIn API integration
- `minimal_llm.py` - Groq LLM processing
- `minimal_enricher.py` - Main enrichment pipeline

### 📊 Export Systems
- `google_sheets_exporter.py` - **PRIMARY**: Automated Google Sheets export
- `csv_exporter.py` - **FALLBACK**: CSV export for manual import
- `complete_pipeline.py` - Full enrichment + export workflow

### 📋 Data Files
- `test_candidates.json` - Sample candidate input
- `enriched_output.json` - Processed candidate data
- `linkedin_permissions_guide.py` - LinkedIn API setup guide

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Activate virtual environment
.\comp\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements_minimal.txt
```

### 2. Configure API Keys
Update `minimal_config.py` with your credentials:
- Composio API Key
- Groq API Key  
- Google Sheets credentials
- LinkedIn connection

### 3. Run Complete Pipeline
```bash
# Enrich candidates and export to Google Sheets
python complete_pipeline.py

# Or run individual steps:
python minimal_enricher.py      # Enrich candidates
python google_sheets_exporter.py # Export to Google Sheets
python csv_exporter.py          # Export to CSV
```

## 📊 Usage Examples

### Google Sheets Export (Recommended)
```bash
python google_sheets_exporter.py
```
- ✅ Creates new Google Sheet automatically
- ✅ Populates with all candidate data
- ✅ Returns shareable URL
- ✅ Professional formatting

### CSV Export (Fallback)
```bash
python csv_exporter.py
```
- ✅ Creates detailed and summary CSV files
- ✅ Compatible with all spreadsheet apps
- ✅ Reliable data export

## 🔧 Technical Details

### Models Used
- **LinkedIn Processing**: `meta-llama/llama-4-maverick-17b-128e-instruct`
- **Google Sheets**: `meta-llama/llama-4-scout-17b-16e-instruct`
- **Fallback**: `llama-3.1-8b-instant`

### Data Flow
1. **Input**: Candidate JSON with basic info
2. **LinkedIn**: Fetch real profile data via Composio
3. **LLM**: Enhance with AI-generated summaries
4. **Export**: Google Sheets or CSV output
5. **Share**: Recruiter-ready candidate profiles

## 🎯 Output Formats

### Google Sheets Columns
- Full Name, Email, Phone, Location
- LinkedIn URL, Title, Industry
- AI-Generated Summary, Experience Highlights
- Key Skills, Career Level, Source, Date

### CSV Files
- **Detailed**: `Recruiter_Candidates_YYYYMMDD_HHMMSS.csv`
- **Summary**: `Recruiter_Summary_YYYYMMDD_HHMMSS.csv`

## 🔒 Security
- All API keys stored in `.env` file
- Google Sheets created under service account
- LinkedIn data fetched via authenticated API
- No sensitive data logged

## 📈 Success Metrics
- ✅ 100% candidate processing success rate
- ✅ LinkedIn profile data for real candidates
- ✅ AI-enhanced summaries and skills
- ✅ Automated Google Sheets creation
- ✅ Recruiter-ready output format

## 🆘 Troubleshooting

### LinkedIn Permissions
Run: `python linkedin_permissions_guide.py`

### Google Sheets Issues
- Check credentials in `minimal_config.py`
- Verify Composio account connections
- Use CSV export as fallback

### Model Errors
- Default model: `meta-llama/llama-4-scout-17b-16e-instruct`
- Fallback: `llama-3.1-8b-instant`
- Check Groq API key validity

## 🔄 Workflow
```
Input JSON → LinkedIn API → LLM Processing → Google Sheets → Recruiter
     ↓              ↓             ↓             ↓
test_candidates → minimal_linkedin → minimal_llm → google_sheets_exporter
```

**Ready for production recruiting workflows!** 🎉