#!/bin/bash

# AI Hiring Prediction System - Production Deployment on Linux

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 AI Hiring Prediction System - Production Deployment${NC}"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Create necessary directories
echo -e "${YELLOW}📁 Creating directories...${NC}"
mkdir -p logs
mkdir -p models
mkdir -p data

# Copy environment file if not exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 Creating .env file from .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env with your production settings${NC}"
fi

# Build and pull images
echo -e "${YELLOW}🐳 Building Docker images...${NC}"
docker-compose build --no-cache

# Remove old containers if running
echo -e "${YELLOW}🛑 Stopping existing containers...${NC}"
docker-compose down || true

# Start services
echo -e "${YELLOW}▶️  Starting services...${NC}"
docker-compose up -d

# Wait for services to be ready
echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"
sleep 10

# Health checks
echo -e "${YELLOW}🏥 Running health checks...${NC}"

BACKEND_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health || echo "000")
FRONTEND_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/ || echo "000")

if [ "$BACKEND_HEALTH" = "200" ]; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
else
    echo -e "${RED}❌ Backend health check failed (HTTP $BACKEND_HEALTH)${NC}"
fi

if [ "$FRONTEND_HEALTH" = "200" ]; then
    echo -e "${GREEN}✅ Frontend is healthy${NC}"
else
    echo -e "${RED}❌ Frontend health check failed (HTTP $FRONTEND_HEALTH)${NC}"
fi

echo ""
echo -e "${GREEN}✨ Deployment complete!${NC}"
echo ""
echo "📊 Service Status:"
docker-compose ps
echo ""
echo "🌐 Access the application:"
echo "  Frontend: http://your-domain.com"
echo "  Backend API: http://your-domain.com:8000"
echo "  API Docs: http://your-domain.com:8000/docs"
echo ""
echo "📋 Useful commands:"
echo "  View logs: docker-compose logs -f backend"
echo "  Stop services: docker-compose down"
echo "  Restart services: docker-compose restart"
echo "  Pull latest images: docker-compose pull"
echo ""
