#!/bin/bash

# AI Hiring Prediction System - Local Docker Deployment

set -e

echo "🐳 Building Docker images..."
docker-compose build

echo "✅ Build complete!"
echo ""
echo "Starting services..."
docker-compose up -d

echo "✅ Services started!"
echo ""
echo "📋 Checking service health..."
sleep 5

# Check backend health
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running: http://localhost:8000"
else
    echo "❌ Backend health check failed"
fi

# Check frontend
if curl -f http://localhost/index.html > /dev/null 2>&1; then
    echo "✅ Frontend is running: http://localhost"
else
    echo "⚠️  Frontend may not be ready yet"
fi

echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "✨ Deployment complete!"
echo ""
echo "Access the application:"
echo "  Frontend: http://localhost"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f backend"
echo "  docker-compose logs -f frontend"
echo ""
echo "To stop services:"
echo "  docker-compose down"
