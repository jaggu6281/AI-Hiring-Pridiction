# AI Hiring Prediction System - Deployment Guide

## 🚀 Deployment Methods

This guide covers multiple deployment options for the AI Hiring Prediction System.

---

## 📋 Prerequisites

- **Docker & Docker Compose** (recommended)
- **Linux Server** (Ubuntu 20.04+ recommended)
- **Minimum 2GB RAM**
- **Minimum 10GB Storage**
- **Python 3.8+** (if deploying without Docker)

---

## 🐳 Option 1: Docker Deployment (Recommended)

### Local Development with Docker

```bash
# Navigate to project directory
cd AI-Hiring-Prediction

# Give permission to deployment script
chmod +x deploy-local.sh

# Run deployment
./deploy-local.sh

# Access the application
# Frontend: http://localhost
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Production Deployment on Linux

```bash
# Give permission to deployment script
chmod +x deploy-production.sh

# Run deployment
./deploy-production.sh

# The script will:
# 1. Check Docker and Docker Compose
# 2. Create necessary directories
# 3. Set up .env file
# 4. Build Docker images
# 5. Start services
# 6. Verify health checks
```

---

## 🌐 Option 2: AWS Deployment (EC2)

### Step 1: Launch EC2 Instance

```bash
# Instance Specifications
- Ubuntu 20.04 LTS
- t3.medium (2 vCPU, 4GB RAM minimum)
- Security Group: Allow ports 80, 443, 8000, 22
- Storage: 20GB+ EBS volume
```

### Step 2: Install Dependencies

```bash
#!/bin/bash

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
sudo apt-get install -y docker.io docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Install Git
sudo apt-get install -y git

# Install Nginx (for reverse proxy)
sudo apt-get install -y nginx
```

### Step 3: Clone and Deploy

```bash
# Clone repository
git clone <your-repo-url> AI-Hiring-Prediction
cd AI-Hiring-Prediction

# Create .env file
cp .env.example .env

# Edit .env with production settings
sudo nano .env

# Deploy
chmod +x deploy-production.sh
./deploy-production.sh
```

### Step 4: Setup Domain (Optional)

```bash
# Install Certbot for SSL
sudo apt-get install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot certonly --standalone -d your-domain.com

# Update nginx configuration to use your domain
sudo nano /etc/nginx/sites-available/default
```

---

## 🔵 Option 3: Google Cloud Run Deployment

### Step 1: Prepare Project

```bash
# Create app.yaml for Cloud Run
cat > app.yaml << EOF
runtime: custom
env: flex
entrypoint: uvicorn backend.main:app --host 0.0.0.0 --port 8080
env_variables:
  PORT: "8080"
EOF
```

### Step 2: Deploy

```bash
# Authenticate with Google Cloud
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Deploy
gcloud app deploy

# View logs
gcloud app logs read -f
```

---

## ☁️ Option 4: Heroku Deployment

### Step 1: Create Procfile

```bash
cat > Procfile << EOF
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
EOF
```

### Step 2: Create runtime.txt

```bash
cat > runtime.txt << EOF
python-3.9.16
EOF
```

### Step 3: Deploy

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set ENVIRONMENT=production

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

---

## 🔐 Security Best Practices

### 1. Environment Variables

```bash
# Never commit .env file
echo ".env" >> .gitignore

# Use strong secret keys
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')
```

### 2. SSL/TLS Certificate

```bash
# Use Let's Encrypt for free SSL
sudo apt-get install -y certbot

# Generate certificate
sudo certbot certonly --standalone -d your-domain.com

# Auto-renew
sudo systemctl enable certbot.timer
```

### 3. Firewall Configuration

```bash
# Allow only necessary ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 4. API Security

```bash
# Enable CORS restrictions
ALLOWED_ORIGINS=https://your-domain.com

# Enable rate limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60
```

---

## 📊 Monitoring & Logging

### Docker Logs

```bash
# Backend logs
docker-compose logs -f backend

# Frontend logs
docker-compose logs -f frontend

# All services
docker-compose logs -f
```

### System Monitoring

```bash
# Install monitoring tools
sudo apt-get install -y htop iotop

# Check disk usage
df -h

# Check memory usage
free -h

# Check CPU usage
top
```

---

## 🔄 Updates & Maintenance

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild Docker images
docker-compose build --no-cache

# Restart services
docker-compose up -d
```

### Database Backups (if applicable)

```bash
# Backup data directory
tar -czf backup-$(date +%Y%m%d).tar.gz data/
```

### Scale Services

```bash
# Increase backend workers
docker-compose up -d --scale backend=3
```

---

## 🐛 Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs backend

# Rebuild container
docker-compose build --no-cache backend
docker-compose up -d backend
```

### Memory Issues

```bash
# Check resource usage
docker stats

# Increase memory limit in docker-compose.yml
# Add: mem_limit: 2g
```

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>

# Or change port in docker-compose.yml
BACKEND_PORT=8001
```

---

## 📞 Support & Troubleshooting

- **Logs**: Check `docker-compose logs -f`
- **Health Check**: Visit `http://localhost:8000/health`
- **Documentation**: http://localhost:8000/docs
- **Issues**: Submit GitHub issues with logs

---

## 🎯 Production Checklist

- [ ] Update `.env` with production settings
- [ ] Enable SSL/TLS certificate
- [ ] Configure domain name
- [ ] Set up monitoring and logging
- [ ] Enable firewall rules
- [ ] Test health endpoints
- [ ] Configure backups
- [ ] Set up log rotation
- [ ] Enable rate limiting
- [ ] Document admin procedures
- [ ] Train team on deployment
- [ ] Set up auto-renewal for SSL
- [ ] Monitor resource usage
- [ ] Test disaster recovery
- [ ] Set up CI/CD pipeline

---

## 🚀 Next Steps

1. **Configure Reverse Proxy**: Set up Nginx/Apache for production
2. **Enable Monitoring**: Use Prometheus, Grafana, or DataDog
3. **Setup Alerts**: Configure notifications for errors
4. **Database**: Add PostgreSQL for persistent data
5. **Cache**: Add Redis for performance
6. **CDN**: Configure CDN for frontend assets
7. **Analytics**: Add analytics to track usage
8. **Backup**: Set up automated backups

---

**Last Updated**: 2026-08-29
**Version**: 1.0.0
