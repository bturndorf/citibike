# Railway Production Deployment Setup

This guide walks you through setting up Railway for production deployment of the CitiBike Rider Probability Application.

## Prerequisites

- GitHub account with your CitiBike repository
- Railway account (free tier available)
- Railway CLI (optional but recommended)

## Step 1: Railway Account Setup

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with your GitHub account
   - This automatically connects your GitHub repositories

2. **Install Railway CLI** (optional)
   ```bash
   npm install -g @railway/cli
   railway login
   ```

## Step 2: Create Railway Project

1. **Create New Project**
   - In Railway dashboard, click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your CitiBike repository

2. **Add Services**
   - **PostgreSQL Database**: Add PostgreSQL service
   - **Backend Service**: Add Python service for FastAPI
   - **Frontend Service**: Add Node.js service for Next.js

## Step 3: Configure Environment Variables

### Backend Environment Variables
Set these in Railway dashboard under your backend service:

```
DATABASE_URL=postgresql://[Railway PostgreSQL URL]
ENVIRONMENT=production
CORS_ORIGINS=["https://your-frontend-domain.railway.app"]
LOG_LEVEL=INFO
```

### Frontend Environment Variables
Set these in Railway dashboard under your frontend service:

```
NEXT_PUBLIC_API_URL=https://your-backend-domain.railway.app
NODE_ENV=production
```

## Step 4: Database Setup

1. **Get Database URL**
   - In Railway dashboard, go to PostgreSQL service
   - Copy the connection string
   - Set it as `DATABASE_URL` in backend environment variables

2. **Run Database Migrations**
   ```bash
   # Connect to Railway backend
   railway connect
   
   # Run migrations
   cd backend
   alembic upgrade head
   ```

3. **Load Data** (if needed)
   ```bash
   # Run data ingestion script
   python load_real_data.py
   ```

## Step 5: Deploy Services

### Option 1: Automatic Deployment (Recommended)
- Railway automatically deploys when you push to your main branch
- Simply push your code:
  ```bash
  git add .
  git commit -m "feat: deploy to Railway"
  git push origin main
  ```

### Option 2: Manual Deployment
Use the provided deployment script:
```bash
./deploy-railway.sh
```

### Option 3: Railway CLI
```bash
# Deploy backend
cd backend
railway up

# Deploy frontend
cd frontend
railway up
```

## Step 6: Configure Domains

1. **Get Service URLs**
   - In Railway dashboard, each service gets a unique URL
   - Backend: `https://your-backend-service.railway.app`
   - Frontend: `https://your-frontend-service.railway.app`

2. **Set Custom Domains** (optional)
   - In Railway dashboard, go to service settings
   - Add custom domain (e.g., `api.citibike-app.com`)
   - Update DNS records as instructed

3. **Update CORS Settings**
   - Update `CORS_ORIGINS` in backend environment variables
   - Include your frontend domain

## Step 7: Verify Deployment

1. **Health Checks**
   - Backend: `https://your-backend.railway.app/api/health`
   - Frontend: `https://your-frontend.railway.app/`

2. **Test API Endpoints**
   - Stations: `GET /api/stations`
   - Probability: `POST /api/probability`

3. **Monitor Logs**
   - In Railway dashboard, check service logs
   - Monitor for errors and performance issues

## Step 8: Production Considerations

### Environment Variables
- Never commit sensitive data to git
- Use Railway's environment variable management
- Keep local `.env` files for development only

### Database Management
- Railway PostgreSQL is managed (backups included)
- Monitor database size and performance
- Consider connection pooling for high traffic

### Scaling
- Railway automatically scales based on traffic
- Monitor resource usage in dashboard
- Upgrade plan if needed for higher limits

### Monitoring
- Railway provides basic monitoring
- Set up alerts for service failures
- Monitor response times and error rates

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check Railway build logs
   - Verify `requirements.txt` and `package.json`
   - Ensure all dependencies are listed

2. **Database Connection Issues**
   - Verify `DATABASE_URL` is correct
   - Check if database service is running
   - Ensure migrations have been run

3. **CORS Errors**
   - Update `CORS_ORIGINS` with correct frontend URL
   - Check frontend API calls use correct backend URL

4. **Environment Variables**
   - Verify all required variables are set
   - Check variable names match code expectations
   - Restart services after changing environment variables

### Useful Commands

```bash
# View Railway logs
railway logs

# Connect to Railway shell
railway connect

# Check service status
railway status

# View environment variables
railway variables
```

## Cost Management

- Railway free tier includes:
  - 500 hours/month of compute
  - 1GB PostgreSQL database
  - 100GB bandwidth
- Monitor usage in Railway dashboard
- Upgrade plan before hitting limits

## Next Steps

1. **Set up monitoring and alerts**
2. **Configure custom domains**
3. **Set up CI/CD for automated testing**
4. **Implement backup strategies**
5. **Plan for scaling**

## Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Project Issues: GitHub repository issues 