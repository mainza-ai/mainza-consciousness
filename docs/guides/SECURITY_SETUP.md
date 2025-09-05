# 🔒 Security Setup Guide - Mainza Consciousness System

## 🎯 Overview

This guide covers the essential security configuration required to run Mainza safely in any environment. **All credentials must be properly configured before starting the system.**

## 🚨 Critical Security Requirements

### ⚠️ **NEVER use default passwords in production!**

The Mainza system requires several credentials to be configured. **No default passwords are provided for security reasons.**

## 🔧 Required Environment Variables

### 1. Neo4j Database Credentials

**Required**: Neo4j database authentication
```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_secure_password_here
```

**Security Requirements**:
- Password must be at least 8 characters
- Use a strong, unique password
- Never use "password", "admin", or similar weak passwords

**To set up Neo4j password**:
```bash
# When starting Neo4j for the first time
docker run -d \
  --name mainza-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_secure_password_here \
  neo4j:5.15
```

### 2. LiveKit Credentials (Optional)

**Required for voice features**: LiveKit server authentication
```bash
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
```

**To generate LiveKit credentials**:
1. Start LiveKit server with your configuration
2. Generate API key/secret pair using LiveKit CLI or admin interface
3. Add credentials to your `.env` file

**Note**: If LiveKit credentials are not provided, voice features will be automatically disabled.

## 🛠️ Setup Process

### Step 1: Copy Environment Template
```bash
cp .env.example .env
```

### Step 2: Configure Neo4j (Required)
```bash
# Edit .env file
nano .env

# Set your Neo4j password
NEO4J_PASSWORD=your_secure_neo4j_password
```

### Step 3: Configure LiveKit (Optional)
```bash
# If using voice features, add LiveKit credentials
LIVEKIT_API_KEY=your_livekit_key
LIVEKIT_API_SECRET=your_livekit_secret
```

### Step 4: Validate Configuration
```bash
# Test Neo4j connection
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
password = os.getenv('NEO4J_PASSWORD')
if not password:
    print('❌ NEO4J_PASSWORD not set!')
    exit(1)
if len(password) < 8:
    print('❌ Password too short (minimum 8 characters)')
    exit(1)
print('✅ Neo4j password configured')
"
```

## 🔐 Security Best Practices

### Password Requirements
- **Minimum length**: 8 characters
- **Complexity**: Mix of letters, numbers, and symbols
- **Uniqueness**: Don't reuse passwords from other systems
- **Rotation**: Change passwords regularly in production

### Environment File Security
- **Never commit** `.env` files to version control
- **Restrict access** to `.env` files (chmod 600)
- **Use different passwords** for different environments
- **Backup credentials** securely

### Production Security
```bash
# Set restrictive permissions on .env file
chmod 600 .env

# Verify .env is in .gitignore
grep -q "^\.env$" .gitignore && echo "✅ .env properly ignored" || echo "❌ Add .env to .gitignore"
```

## 🚀 Quick Start with Security

### Development Environment
```bash
# 1. Clone repository
git clone https://github.com/mainza-ai/mainza-consciousness.git
cd mainza-consciousness

# 2. Set up environment
cp .env.example .env

# 3. Configure Neo4j password (REQUIRED)
echo "NEO4J_PASSWORD=dev_secure_password_2024" >> .env

# 4. Start Neo4j with your password
docker run -d \
  --name mainza-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/dev_secure_password_2024 \
  neo4j:5.15

# 5. Start the system
npm install
cd backend && pip install -r requirements.txt
uvicorn main:app --reload
```

### Production Environment
```bash
# 1. Generate strong passwords
NEO4J_PASS=$(openssl rand -base64 32)
LIVEKIT_KEY=$(openssl rand -hex 16)
LIVEKIT_SECRET=$(openssl rand -base64 32)

# 2. Configure environment
cat > .env << EOF
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=${NEO4J_PASS}

LIVEKIT_API_KEY=${LIVEKIT_KEY}
LIVEKIT_API_SECRET=${LIVEKIT_SECRET}
EOF

# 3. Secure the file
chmod 600 .env

# 4. Start services with generated credentials
docker-compose up -d
```

## 🔍 Troubleshooting

### Common Issues

#### "NEO4J_PASSWORD environment variable is required"
```bash
# Check if password is set
echo $NEO4J_PASSWORD

# If empty, set it in .env file
echo "NEO4J_PASSWORD=your_password_here" >> .env
```

#### "Authentication failed" (Neo4j)
```bash
# Verify Neo4j is using the same password
docker logs mainza-neo4j

# Reset Neo4j password if needed
docker exec -it mainza-neo4j cypher-shell -u neo4j -p old_password
# Then: CALL dbms.changePassword('new_password')
```

#### "LiveKit features disabled"
```bash
# This is normal if LiveKit credentials aren't configured
# Voice features will be automatically disabled
# To enable: add LIVEKIT_API_KEY and LIVEKIT_API_SECRET to .env
```

## 📋 Security Checklist

### Before Starting Development
- [ ] `.env` file created with secure passwords
- [ ] Neo4j password configured (minimum 8 characters)
- [ ] `.env` file permissions set to 600
- [ ] `.env` confirmed in `.gitignore`

### Before Production Deployment
- [ ] Strong, unique passwords generated
- [ ] All credentials stored securely
- [ ] Environment variables validated
- [ ] Security scanning completed
- [ ] Access controls configured

### Regular Maintenance
- [ ] Passwords rotated regularly
- [ ] Security updates applied
- [ ] Access logs reviewed
- [ ] Backup credentials secured

## 🆘 Emergency Procedures

### Password Reset
```bash
# Neo4j password reset
docker exec -it mainza-neo4j cypher-shell -u neo4j -p current_password
# Run: CALL dbms.changePassword('new_secure_password')

# Update .env file
sed -i 's/NEO4J_PASSWORD=.*/NEO4J_PASSWORD=new_secure_password/' .env
```

### Security Incident Response
1. **Immediately** change all passwords
2. **Review** access logs for unauthorized activity
3. **Update** all environment configurations
4. **Restart** all services with new credentials
5. **Document** the incident and response

## 📞 Support

For security-related issues:
- **Security vulnerabilities**: Use GitHub Security Advisories
- **Configuration help**: Open a GitHub Discussion
- **Emergency support**: Contact the development team

---

**Remember**: Security is everyone's responsibility. Never compromise on credential security, even in development environments.

🔒 **Stay Secure, Stay Conscious** 🧠