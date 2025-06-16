# Vercel + Supabase Setup Guide

## Overview

This guide provides step-by-step instructions for setting up Vercel and Supabase for the CitiBike Rider Probability Application migration.

## Prerequisites

- GitHub repository with the CitiBike project
- Local PostgreSQL database with CitiBike data (3.1M trips, 2,234 stations, station_mapping)
- Railway deployment running (for rollback purposes)

## Step 1: Vercel Account Setup

### 1.1 Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Click "Sign Up" and create an account (GitHub OAuth recommended)
3. Verify your email address

### 1.2 Connect GitHub Repository
1. In Vercel dashboard, click "New Project"
2. Select "Import Git Repository"
3. Choose your CitiBike GitHub repository
4. Vercel will automatically detect Next.js and Python configurations

### 1.3 Configure Vercel Project
1. **Project Name**: `citibike-rider-probability`
2. **Framework Preset**: Next.js (auto-detected)
3. **Root Directory**: `./` (root of repository)
4. **Build Command**: Leave as default
5. **Output Directory**: Leave as default
6. **Install Command**: Leave as default

### 1.4 Set Environment Variables
In Vercel dashboard, go to Project Settings → Environment Variables:

```
DATABASE_URL=your_supabase_database_url_here
NEXT_PUBLIC_API_URL=https://your-vercel-domain.vercel.app/api
```

## Step 2: Supabase Database Setup

### 2.1 Create Supabase Account
1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project" and create an account
3. Verify your email address

### 2.2 Create New Project
1. Click "New Project"
2. **Organization**: Create new or select existing
3. **Project Name**: `citibike-rider-probability`
4. **Database Password**: Create a strong password
5. **Region**: Choose closest to your users (e.g., US East for NYC data)
6. Click "Create new project"

### 2.3 Get Database Connection String
1. In Supabase dashboard, go to Settings → Database
2. Copy the "Connection string" (URI format)
3. It should look like: `postgresql://postgres:[password]@[host]:5432/postgres`

### 2.4 Set Supabase Environment Variables
In Vercel dashboard, add the Supabase connection string:

```
SUPABASE_DATABASE_URL=postgresql://postgres:[password]@[host]:5432/postgres
```

## Step 3: Database Migration

### 3.1 Prepare Migration Script
The migration script is located at `utils/migration/migrate_to_supabase.py`

### 3.2 Set Local Environment Variables
Create a `.env` file in the project root:

```bash
# Local database (for source)
LOCAL_DATABASE_URL=postgresql://localhost/dev

# Supabase database (for target)
SUPABASE_DATABASE_URL=postgresql://postgres:[password]@[host]:5432/postgres
```

### 3.3 Run Migration
```bash
cd utils/migration
python migrate_to_supabase.py
```

### 3.4 Verify Migration
The script will automatically verify:
- Row counts match between local and Supabase
- Sample queries work correctly
- Data integrity is maintained

## Step 4: Backend Deployment

### 4.1 Update Backend Configuration
The backend is already configured with `backend/vercel.json` for serverless deployment.

### 4.2 Deploy Backend
1. Push changes to GitHub
2. Vercel will automatically deploy the backend
3. Check deployment logs in Vercel dashboard

### 4.3 Test Backend Endpoints
Test the following endpoints:
- `GET /api/health` - Health check
- `GET /api/stations` - List stations
- `POST /api/probability` - Calculate probability

## Step 5: Frontend Deployment

### 5.1 Update Frontend Configuration
The frontend is already configured with `frontend/vercel.json` for Next.js deployment.

### 5.2 Update API Endpoints
In the frontend code, update API calls to use the new Vercel backend URL:

```javascript
// Update in frontend components
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://your-vercel-domain.vercel.app/api';
```

### 5.3 Deploy Frontend
1. Push changes to GitHub
2. Vercel will automatically deploy the frontend
3. Check deployment logs in Vercel dashboard

### 5.4 Test Frontend
Test the complete user workflow:
1. Load the application
2. Select a station from the dropdown
3. Submit probability calculation
4. Verify results display correctly

## Step 6: Integration Testing

### 6.1 End-to-End Testing
1. **Station Selection**: Verify combobox loads with Supabase data
2. **Probability Calculation**: Test with known stations
3. **Data Integrity**: Compare results with local development
4. **Performance**: Check response times

### 6.2 Performance Testing
- Load time for station list
- Probability calculation response time
- Database query performance
- Memory usage

### 6.3 Error Handling
- Test with invalid station names
- Test with network failures
- Test with database connection issues

## Step 7: Production Configuration

### 7.1 Custom Domain (Optional)
1. In Vercel dashboard, go to Settings → Domains
2. Add your custom domain
3. Configure DNS settings
4. Update environment variables if needed

### 7.2 Monitoring Setup
1. Enable Vercel Analytics
2. Set up error tracking
3. Monitor performance metrics

### 7.3 Security Configuration
1. Review Supabase security settings
2. Configure CORS settings
3. Set up API rate limiting if needed

## Step 8: Railway Cleanup

### 8.1 Verify Vercel Deployment
Before shutting down Railway:
1. Confirm all functionality works on Vercel
2. Test with real users if possible
3. Monitor for any issues

### 8.2 Export Final Railway Data
```bash
# Backup Railway data one final time
railway variables --service Postgres
```

### 8.3 Remove Railway Configuration
1. Delete `railway.json` files
2. Remove Railway CLI dependencies
3. Archive Railway-specific documentation

### 8.4 Shutdown Railway
1. In Railway dashboard, go to project settings
2. Click "Delete Project"
3. Confirm deletion

## Troubleshooting

### Common Issues

#### Database Connection Issues
- Verify Supabase connection string format
- Check firewall settings
- Ensure database is accessible from Vercel

#### Deployment Failures
- Check Vercel build logs
- Verify Python dependencies in `requirements.txt`
- Check Next.js build configuration

#### Performance Issues
- Monitor database query performance
- Check Vercel function timeout settings
- Optimize database indexes if needed

#### Environment Variable Issues
- Verify all environment variables are set in Vercel
- Check variable names match code expectations
- Ensure sensitive data is properly secured

### Support Resources
- [Vercel Documentation](https://vercel.com/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [Vercel Community](https://github.com/vercel/vercel/discussions)
- [Supabase Community](https://github.com/supabase/supabase/discussions)

## Migration Checklist

- [ ] Vercel account created and configured
- [ ] Supabase project created and configured
- [ ] Database migration completed successfully
- [ ] Backend deployed to Vercel
- [ ] Frontend deployed to Vercel
- [ ] All API endpoints working
- [ ] Complete user workflow tested
- [ ] Performance verified
- [ ] Error handling tested
- [ ] Railway deployment verified as backup
- [ ] Railway configuration removed
- [ ] Documentation updated
- [ ] Team notified of new deployment

## Rollback Plan

If issues arise during migration:

1. **Immediate Rollback**: Keep Railway deployment running
2. **Data Recovery**: Use local PostgreSQL as backup
3. **Configuration Recovery**: Restore from git history
4. **User Communication**: Notify users of temporary issues

## Success Criteria

- [ ] Application functions identically to Railway deployment
- [ ] Performance is equal to or better than Railway
- [ ] Zero data loss during migration
- [ ] Development velocity improved
- [ ] Reliable deployment process established 