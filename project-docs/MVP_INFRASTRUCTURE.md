# MVP Infrastructure Plan: Simplified Approach

## 1. MVP Infrastructure Overview

### 1.1 Simplified Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Data Storage  │
│   (Vercel/Netlify)│◄──►│   (Railway/Render)│◄──►│   (Railway Postgres)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 1.2 MVP Infrastructure Choices

#### Option 1: Railway (Recommended for MVP)
- **Frontend**: Deploy Next.js app directly to Railway
- **Backend**: Python FastAPI app on Railway
- **Database**: Railway PostgreSQL (included)
- **Storage**: Railway file storage or simple S3 bucket
- **Cost**: ~$5-10/month for MVP
- **Pros**: Simple deployment, integrated database, good free tier
- **Cons**: Less control than AWS

#### Option 2: Render (Alternative)
- **Frontend**: Static site hosting on Render
- **Backend**: Python web service on Render
- **Database**: Render PostgreSQL
- **Cost**: ~$7-15/month for MVP
- **Pros**: Good free tier, simple setup
- **Cons**: Slightly more complex than Railway

#### Option 3: Heroku (Classic Choice)
- **Frontend**: Static site hosting
- **Backend**: Python dyno
- **Database**: Heroku Postgres
- **Cost**: ~$7-25/month for MVP
- **Pros**: Well-established, good documentation
- **Cons**: Removed free tier, more expensive

## 2. Simplified MVP Setup

### 2.1 Railway Setup (Recommended)

#### Step 1: Railway Account Setup
1. Create Railway account (railway.app)
2. Connect GitHub repository
3. Set up project

#### Step 2: Database Setup
1. Add PostgreSQL service to Railway project
2. Get connection string from Railway dashboard
3. No complex VPC or security groups needed

#### Step 3: Backend Deployment
1. Create `railway.json` configuration
2. Railway auto-detects Python app
3. Deploy with `git push`

#### Step 4: Frontend Deployment
1. Deploy Next.js app to Railway
2. Configure environment variables
3. Get live URL automatically

### 2.2 Simplified Data Pipeline

#### Data Ingestion (One-time)
```python
# Simple script to run locally or on Railway
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Download CitiBike data
def download_data():
    # Download 3-6 months of data for MVP
    # Process and clean data
    # Load to Railway PostgreSQL
    pass
```

#### Database Schema (Simplified)
```sql
-- Simple MVP schema
CREATE TABLE stations (
    id SERIAL PRIMARY KEY,
    station_id VARCHAR(50) UNIQUE,
    name VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8)
);

CREATE TABLE trips (
    id SERIAL PRIMARY KEY,
    bike_id VARCHAR(50),
    start_station_id VARCHAR(50),
    end_station_id VARCHAR(50),
    started_at TIMESTAMP,
    ended_at TIMESTAMP
);
```

## 3. MVP Development Workflow

### 3.1 Local Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### 3.2 Simple Deployment
```bash
# Railway deployment (automatic with git push)
git add .
git commit -m "Update MVP"
git push origin main

# Railway automatically deploys
```

### 3.3 Environment Variables
```bash
# Railway dashboard or .env file
DATABASE_URL=postgresql://...
API_KEY=your_api_key
FRONTEND_URL=https://your-app.railway.app
```

## 4. MVP Monitoring (Minimal)

### 4.1 Basic Error Tracking
```python
# Simple logging for debugging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log errors for debugging
try:
    # Your code
    pass
except Exception as e:
    logger.error(f"Error: {e}")
```

### 4.2 Railway Dashboard
- Built-in logs and metrics
- No additional monitoring setup needed
- Basic performance insights included

## 5. Simplified Project Structure

```
citibike-mvp/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── requirements.txt     # Python dependencies
│   ├── models.py           # Database models
│   ├── data_ingestion.py   # One-time data load
│   └── probability.py      # Simple probability model
├── frontend/
│   ├── package.json        # Node dependencies
│   ├── pages/
│   │   ├── index.tsx       # Home page
│   │   └── calculate.tsx   # Calculator page
│   └── components/
│       ├── StationMap.tsx  # Simple map component
│       └── Results.tsx     # Results display
├── data/
│   └── citibike_data/      # Downloaded data files
└── README.md
```

## 6. MVP Timeline (Simplified)

### Week 1: Basic Setup
- Set up Railway account and project
- Create basic database schema
- Deploy simple "Hello World" backend

### Week 2: Data Ingestion
- Download sample CitiBike data
- Create data processing script
- Load initial dataset

### Week 3: Basic Backend
- Create simple probability calculation
- Build basic API endpoints
- Test with sample data

### Week 4: Frontend
- Create simple Next.js app
- Add basic form for parameters
- Display probability results

### Week 5: Integration & Testing
- Connect frontend to backend
- Test end-to-end functionality
- Deploy to production

## 7. Cost Breakdown (MVP)

### Railway (Recommended)
- **Database**: $5/month (1GB storage)
- **Backend**: $5/month (512MB RAM)
- **Frontend**: Free (static hosting)
- **Total**: ~$10/month

### Render (Alternative)
- **Database**: $7/month
- **Backend**: $7/month
- **Frontend**: Free
- **Total**: ~$14/month

## 8. MVP Success Criteria

### Technical Success
- Application runs without errors
- Probability calculations work correctly
- Users can input parameters and see results
- Deployment process is simple and reliable

### User Success
- Users understand how to use the app
- Results are presented clearly
- App provides value to CitiBike users

### Business Success
- App gains some user traction
- Positive feedback from initial users
- Foundation for future enhancements

## 9. Future Scaling (When Needed)

### When to Add Complexity
- **More than 100 daily users**: Add caching
- **Database performance issues**: Optimize queries
- **Need for real-time data**: Add scheduled jobs
- **Advanced features**: Add user accounts

### Migration Path
- Start with Railway MVP
- Move to AWS when needed
- Gradual feature addition
- Maintain simple deployment process

This simplified approach focuses on getting a working MVP quickly without the complexity of AWS, CI/CD, or advanced monitoring. We can always add these features later when the application proves successful and needs to scale. 