# Security Guidelines

## 🚨 CRITICAL: API Key Security

### **NEVER COMMIT API KEYS TO THE REPOSITORY**

API keys are **CREDENTIALS** and must be treated as **SECRETS**. Exposing them in code repositories is a **CRITICAL SECURITY BREACH**.

## 🔒 API Key Management

### **1. Environment Variables Only**

```bash
# ✅ CORRECT: Use environment variables
export OPENAI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"
export GOOGLE_API_KEY="your-key-here"
```

### **2. .env Files (Local Only)**

```bash
# ✅ CORRECT: .env file (add to .gitignore)
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
GOOGLE_API_KEY=your-key-here
```

### **3. 1Password Integration**

```bash
# ✅ CORRECT: Use 1Password CLI
op item get "OpenAI API Key" --fields api_key
op item get "Anthropic API Key" --fields api_key
```

## 🚫 What NOT to Do

### **❌ NEVER:**

- Hardcode API keys in source code
- Commit API keys to git
- Store API keys in JSON files
- Include API keys in documentation
- Share API keys in chat logs
- Store API keys in cache files

### **❌ Examples of WRONG:**

```python
# WRONG: Hardcoded API key
api_key = "sk-1234567890abcdef1234567890abcdef1234567890abcdef"

# WRONG: API key in config file
config = {
    "openai_key": "sk-1234567890abcdef1234567890abcdef1234567890abcdef"
}
```

## 🛡️ Security Checklist

### **Before Committing:**

- [ ] No API keys in source code
- [ ] No API keys in config files
- [ ] No API keys in documentation
- [ ] No API keys in cache files
- [ ] No API keys in test files (use placeholders)
- [ ] .gitignore includes sensitive files

### **Sensitive Files to Ignore:**

```
# Add to .gitignore
.env
*.env
.env.local
.env.production
.env.staging
api_discovery_cache.json
working_apis_cache.json
cost_history.json
*.cache.json
secrets.json
credentials.json
```

## 🔍 Security Scanning

### **Regular Security Checks:**

```bash
# Scan for potential API keys
grep -r "sk-" . --exclude-dir=.git
grep -r "AKIA" . --exclude-dir=.git
grep -r "ghp_" . --exclude-dir=.git

# Scan for environment variable patterns
grep -r "export.*API_KEY" . --exclude-dir=.git
```

## 🚨 Incident Response

### **If API Keys Are Exposed:**

1. **IMMEDIATELY REVOKE** the exposed API keys
2. **DELETE** the files containing the keys
3. **UPDATE** .gitignore to prevent future exposure
4. **SCAN** the entire repository for other exposures
5. **DOCUMENT** the incident and lessons learned
6. **TRAIN** team members on security practices

## 📚 Best Practices

### **1. Use Placeholders in Examples**

```python
# ✅ CORRECT: Use placeholders
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")
```

### **2. Validate Environment Variables**

```python
# ✅ CORRECT: Validate at startup
required_vars = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {missing_vars}")
```

### **3. Use Configuration Management**

```python
# ✅ CORRECT: Use proper config management
from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    anthropic_api_key: str
    
    class Config:
        env_file = ".env"
```

## 🔐 Additional Security Measures

### **1. API Key Rotation**

- Rotate API keys regularly
- Use different keys for different environments
- Monitor API key usage for anomalies

### **2. Access Control**

- Limit API key permissions to minimum required
- Use service accounts when possible
- Monitor and log all API usage

### **3. Secure Development**

- Use pre-commit hooks to scan for secrets
- Integrate security scanning in CI/CD
- Regular security audits of codebase

## 📞 Security Contacts

If you discover a security issue:

1. **DO NOT** create a public issue
2. **DO NOT** discuss in public channels
3. **IMMEDIATELY** contact the security team
4. **FOLLOW** the incident response plan

---

**Remember: Security is everyone's responsibility. When in doubt, ask before committing sensitive information.**
