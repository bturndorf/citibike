#!/bin/bash

# Railway Deployment Script for CitiBike Application
echo "🚂 Starting Railway deployment..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Please install it first:"
    echo "npm install -g @railway/cli"
    exit 1
fi

# Login to Railway (if not already logged in)
echo "🔐 Logging into Railway..."
railway login

# Deploy backend
echo "🔧 Deploying backend..."
cd backend
railway up --service backend
cd ..

# Deploy frontend
echo "🎨 Deploying frontend..."
cd frontend
railway up --service frontend
cd ..

echo "✅ Deployment complete!"
echo "🌐 Check your Railway dashboard for deployment status and URLs" 