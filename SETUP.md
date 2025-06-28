# 🔧 Environment Setup Guide

## 🚀 Quick Start

### 1. Environment Variables Setup

**Required**: Copy the template and configure your API keys
```bash
cp env.template .env
```

Then edit `.env` file with your actual values:

```properties
# Supabase Configuration (Required for chat monitoring)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key

# GitHub Configuration (Required for automation)
GITHUB_TOKEN=ghp_your_github_personal_access_token
GITHUB_USER=your_github_username
GITHUB_REPO=your_username/your_repo_name

# API Keys (Optional but recommended)
GROQ_API_KEY=gsk_your_groq_api_key
OPENAI_API_KEY=sk-your_openai_api_key
```

### 2. Install Dependencies

```bash
# Python dependencies
pip install -r requirements-test.txt

# Node.js dependencies (if needed)
npm install
```

### 3. Run Tests

```bash
# Run all offline tests
pytest tests/ -v -m offline

# Run specific test categories
pytest tests/unit/ -v
pytest tests/integration/ -v -m offline
pytest tests/e2e/ -v -m offline
```

### 4. Start Development

```bash
# Run the main automation system
python tests/Feature/copilot_github_cli_automation.py
```

## 📋 Required API Keys & Services

### Essential Services
- **Supabase**: For chat message monitoring and data storage
- **GitHub**: For repository management and issue automation
- **GitHub CLI**: Install with `gh auth login`

### Optional Services
- **Groq API**: For AI-powered responses
- **OpenAI API**: Alternative AI provider
- **JIRA**: For project management integration
- **n8n**: For workflow automation
- **LINE Bot**: For messaging integration

## 🔒 Security Notes

- ⚠️ **Never commit `.env` files to git**
- 🔑 **Keep API keys secure and rotate regularly**
- 🛡️ **Use environment-specific configurations**
- 📝 **Review `.gitignore` to ensure secrets are excluded**

## 🏃‍♂️ Running the System

### Local Development
```bash
# Start with offline mode for testing
python tests/Feature/copilot_github_cli_automation.py --offline

# Start with full online integration
python tests/Feature/copilot_github_cli_automation.py
```

### Testing Integration
```bash
# Test Supabase connection
pytest tests/integration/ -v -k supabase

# Test GitHub integration
pytest tests/integration/ -v -k github

# Test complete workflow
pytest tests/e2e/ -v
```

## 🔧 Configuration Options

### Debug Mode
```properties
DEBUG=true
LOG_LEVEL=DEBUG
ENVIRONMENT=development
```

### Production Mode
```properties
DEBUG=false
LOG_LEVEL=INFO
ENVIRONMENT=production
```

## 📞 Support

If you encounter issues:
1. Check your `.env` configuration
2. Verify API key permissions
3. Run `pytest tests/ -v -m offline` to test core functionality
4. Check the latest documentation in project README

---

🎯 **Ready to automate!** Your GitHub Copilot development automation system is configured.
