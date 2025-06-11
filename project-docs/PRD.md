# Product Requirements Document: CitiBike Rider Probability Application

## 1. Executive Summary

### 1.1 Product Overview
A web application that estimates the probability that a NYC CitiBike rider has ridden the same bike twice, based on their riding patterns and station preferences.

### 1.2 Problem Statement
CitiBike users often wonder about the likelihood of encountering the same bike multiple times during their rides. This application provides a data-driven answer to this question by analyzing historical CitiBike usage patterns.

## 2. Product Requirements

### 2.1 Core Features

#### 2.1.1 Data Ingestion Layer
- **Requirement**: One-time ingestion of CitiBike historical data
- **Data Sources**: 
  - CitiBike trip history data (https://citibikenyc.com/system-data)
  - Real-time station data (GBFS feed)
- **Data Processing**: 
  - Clean and normalize trip data
  - Extract bike IDs, station information, timestamps
  - Calculate bike movement patterns
  - Store in structured database format

#### 2.1.2 Statistical Modeling Layer
- **Requirement**: Calculate probability of encountering same bike twice
- **Input Parameters**:
  - User's home station(s)
  - Riding frequency (rides per week/month)
  - Time patterns (weekday vs weekend, time of day)
  - Station preferences
  - Date range for analysis
- **Modeling Approach**:
  - Monte Carlo simulation based on historical bike movement patterns
  - Probability calculations using bike distribution data
  - Confidence intervals for estimates

#### 2.1.3 Frontend Interface
- **Requirement**: User-friendly web interface for parameter input and results display
- **Features**:
  - Parameter input forms
  - **Alphabetized combobox dropdown for station selection** (MVP)
  - Probability visualization (charts/graphs)
  - Results explanation and insights
  - Mobile-responsive design
  - (Future) Interactive station selection (map-based)

### 2.2 Technical Requirements

#### 2.2.1 Infrastructure
- **Platform**: Railway (PostgreSQL, file storage) for MVP
- **Deployment**: Simple git push deployment (no complex CI/CD needed)
- **Scalability**: Railway handles automatic scaling
- **Monitoring**: Railway dashboard monitoring (basic)

#### 2.2.2 Data Requirements
- **Storage**: PostgreSQL database for structured data (Railway)
- **Processing**: Python for data analysis and modeling
- **API**: RESTful API for frontend-backend communication
- **Caching**: Simple in-memory caching (no Redis for MVP)

#### 2.2.3 Security Requirements
- **Data Privacy**: No personal user data collection
- **API Security**: Rate limiting and input validation
- **Infrastructure**: Railway security best practices

### 2.3 Non-Functional Requirements

#### 2.3.1 Performance
- **Response Time**: < 3 seconds for probability calculations
- **Availability**: 99.5% uptime

#### 2.3.2 Usability
- **User Experience**: Intuitive interface for non-technical users
- **Accessibility**: WCAG 2.1 AA compliance
- **Mobile**: Responsive design for mobile devices

#### 2.3.3 Maintainability
- **Code Quality**: Clean, documented, testable code
- **Monitoring**: Comprehensive logging and error tracking
- **Updates**: Easy deployment of new features and bug fixes

## 3. User Stories

### 3.1 Primary User Journey
1. **User visits the application**
   - Sees clear explanation of what the app does
   - Understands how to use the interface

2. **User inputs their parameters**
   - Selects their home station from an **alphabetized combobox dropdown**
   - Specifies their riding frequency
   - Chooses time patterns and preferences

3. **User receives probability estimate**
   - Sees calculated probability with confidence interval
   - Gets explanation of the calculation
   - Views supporting visualizations

4. **User explores different scenarios**
   - Adjusts parameters to see how probability changes
   - Compares different station combinations
   - Saves or shares results

### 3.2 User Personas

#### 3.2.1 Casual Rider (Primary)
- **Profile**: Rides 1-3 times per week
- **Goals**: Understand likelihood of bike encounters
- **Technical Level**: Basic computer skills

#### 3.2.2 Frequent Rider (Secondary)
- **Profile**: Rides 5+ times per week
- **Goals**: Optimize station choices for bike variety
- **Technical Level**: Comfortable with data analysis

## 4. Technical Architecture

### 4.1 System Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Data Layer    │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (PostgreSQL)  │
│   (Railway)     │    │   (Railway)     │    │   (Railway)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │   Modeling      │
                       │   (Python)      │
                       └─────────────────┘
```

### 4.2 Technology Stack Recommendations

#### 4.2.1 Frontend
- **Framework**: Next.js with React
- **Styling**: Tailwind CSS
- **Maps**: Mapbox or Google Maps API (future enhancement)
- **Charts**: Chart.js or D3.js
- **Deployment**: Railway static hosting

#### 4.2.2 Backend
- **Language**: Python 3.9+
- **Framework**: FastAPI
- **Database ORM**: SQLAlchemy
- **Data Processing**: Pandas, NumPy
- **Statistical Modeling**: SciPy, scikit-learn
- **Deployment**: Railway Python service

#### 4.2.3 Infrastructure (MVP)
- **Platform**: Railway.app
- **Database**: Railway PostgreSQL (included)
- **Storage**: Railway file storage or simple S3 bucket
- **Deployment**: Simple git push (no CI/CD needed)
- **Cost**: ~$10/month for MVP
- **Scaling**: Railway handles scaling automatically

#### 4.2.4 Future Infrastructure (Post-MVP)
- **Compute**: AWS EC2 (when scaling beyond Railway)
- **Database**: AWS RDS PostgreSQL
- **Storage**: AWS S3 for data files
- **Caching**: AWS ElastiCache Redis
- **Deployment**: AWS Elastic Beanstalk or Docker on EC2

## 5. MVP Scope

### 5.1 MVP Features
1. **Data Ingestion**: One-time import of 3-6 months of CitiBike data
2. **Basic Modeling**: Simple probability calculation based on station proximity
3. **Frontend**: Basic form for parameter input and results display (with alphabetized combobox dropdown for station selection)
4. **Deployment**: Railway platform with simple git push deployment

### 5.2 MVP Limitations
- Limited to Manhattan and Brooklyn data
- Basic probability model (no advanced statistical methods)
- No user accounts or saved preferences
- Basic UI without advanced visualizations
- No complex CI/CD pipeline (simple git push deployment)
- **No map-based station selection in MVP**

## 6. Future Enhancements

### 6.1 Phase 2 Features
- Monte Carlo modeling
- **Map-based station selection**

### 6.2 Phase 3 Features
- Real-time data updates
- Advanced visualizations and insights

## 7. Success Criteria

### 7.1 Technical Success
- Application successfully ingests and processes CitiBike data
- Probability calculations are mathematically sound
- Application is stable and performs well under load
- Simple deployment process works reliably (git push to Railway)

### 7.2 User Success
- Users can easily input their parameters
- Results are presented clearly and understandably
- Users find the probability estimates useful and accurate