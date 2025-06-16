# Railway to Vercel + Supabase Migration Plan

## Migration Overview

**Objective**: Migrate CitiBike Rider Probability Application from Railway to Vercel + Supabase
**Goal**: Eliminate Railway debugging time and improve development velocity
**Scope**: Complete platform migration with zero data loss
**Timeline**: 1-2 days total migration time
**Branch**: `migration/railway-to-vercel-supabase`

## Migration Rationale

### Railway Issues
- Deploy failures and inconsistent behavior
- PostgreSQL service problems and storage constraints
- Complex debugging and troubleshooting requirements
- Limited development velocity due to platform issues

### Vercel + Supabase Benefits
- **Vercel**: Excellent Next.js support, fast deployments, reliable infrastructure
- **Supabase**: Better PostgreSQL management, real-time features, superior reliability
- **Development Velocity**: Eliminate Railway debugging time, focus on application features
- **Simplified Deployment**: Git push deployment with automatic scaling

## Current Architecture (Railway)

```
GitHub Repository
       ↓
   Railway.app
       ↓
┌─────────────────┐
│   Frontend      │  Next.js app (Railway)
│   (Railway)     │
└─────────────────┘
       ↓
┌─────────────────┐
│   Backend       │  FastAPI app (Railway)
│   (Railway)     │
└─────────────────┘
       ↓
┌─────────────────┐
│   PostgreSQL    │  Railway PostgreSQL
│   (Railway)     │
└─────────────────┘
```

## Target Architecture (Vercel + Supabase)

```
GitHub Repository
       ↓
   Vercel.app
       ↓
┌─────────────────┐
│   Frontend      │  Next.js app (Vercel)
│   (Vercel)      │
└─────────────────┘
       ↓
┌─────────────────┐
│   Backend       │  FastAPI serverless functions (Vercel)
│   (Vercel)      │
└─────────────────┘
       ↓
┌─────────────────┐
│   PostgreSQL    │  Supabase database
│   (Supabase)    │
└─────────────────┘
```

## Migration Tasks

### Phase 1: Pre-Migration Preparation ✅ COMPLETED

#### Task 1.1: Data Backup and Documentation ✅ COMPLETED
- [x] Document current Railway setup
- [x] Railway data already available locally (3.1M trips, 2,234 stations, station_mapping)
- [x] Local PostgreSQL database with complete dataset
- [x] Database schema and indexes already documented
- [x] Environment variables documented

#### Task 1.2: Migration Planning ✅ COMPLETED
- [x] Create migration branch
- [x] Document current architecture
- [x] Plan rollback strategy
- [x] Create migration timeline
- [x] Identify potential risks and mitigation strategies

### Phase 2: Vercel + Supabase Setup 🔄 IN PROGRESS

#### Task 2.1: Vercel Account and Project Setup
- [ ] Create Vercel account (vercel.com)
- [ ] Connect GitHub repository to Vercel
- [ ] Create new Vercel project
- [ ] Configure Vercel project settings
- [ ] Set up Vercel CLI (if needed)

#### Task 2.2: Supabase Database Setup
- [ ] Create Supabase account (supabase.com)
- [ ] Create new Supabase project
- [ ] Get PostgreSQL connection string from dashboard
- [ ] Test database connectivity
- [ ] Configure Supabase environment variables

#### Task 2.3: Basic Backend Deployment Test
- [ ] Create simple FastAPI "Hello World" app
- [ ] Deploy to Vercel Serverless Functions
- [ ] Verify deployment works
- [ ] Test basic API endpoints

### Phase 3: Database Migration

#### Task 3.1: Supabase Schema Setup
- [ ] Create database schema in Supabase
  - [ ] stations table
  - [ ] trips table
  - [ ] station_mapping table
- [ ] Set up database indexes for performance
- [ ] Configure database constraints and relationships
- [ ] Test schema with sample data

#### Task 3.2: Data Migration Execution
- [ ] Import 3.1M trips from local PostgreSQL to Supabase
- [ ] Import 2,234 stations data
- [ ] Import station_mapping data
- [ ] Verify data integrity after migration
- [ ] Test database queries and performance
- [ ] Create database indexes for optimal performance

#### Task 3.3: Database Connection Updates
- [ ] Update backend code to use Supabase PostgreSQL connection
- [ ] Update environment variables for Supabase DATABASE_URL
- [ ] Test database connectivity from local development
- [ ] Verify Alembic migrations work with Supabase
- [ ] Update test database configuration for Supabase

### Phase 4: Backend Migration

#### Task 4.1: FastAPI to Vercel Serverless Functions
- [ ] Convert FastAPI app to Vercel serverless functions
- [ ] Update API routes for Vercel serverless architecture
- [ ] Configure vercel.json for Python runtime
- [ ] Update requirements.txt for Vercel compatibility
- [ ] Test API endpoints in Vercel environment

#### Task 4.2: Environment Variable Migration
- [ ] Migrate Railway environment variables to Vercel
- [ ] Update DATABASE_URL to point to Supabase
- [ ] Configure CORS settings for Vercel deployment
- [ ] Set up production environment variables
- [ ] Test environment variable access in Vercel

#### Task 4.3: API Endpoint Testing
- [ ] Test all API endpoints in Vercel environment
- [ ] Verify probability calculation endpoint works
- [ ] Test stations endpoint with Supabase data
- [ ] Validate error handling and response formats
- [ ] Performance testing with real CitiBike data

### Phase 5: Frontend Migration

#### Task 5.1: Next.js to Vercel Deployment
- [ ] Deploy Next.js frontend to Vercel
- [ ] Update API endpoint URLs to point to Vercel backend
- [ ] Configure Vercel build settings for Next.js
- [ ] Set up environment variables for frontend
- [ ] Test frontend deployment and functionality

#### Task 5.2: API Integration Updates
- [ ] Update frontend API calls to use Vercel backend URLs
- [ ] Test station combobox with Supabase data
- [ ] Verify probability calculation workflow
- [ ] Test error handling and loading states
- [ ] Validate complete user journey

#### Task 5.3: Frontend-Backend Integration Testing
- [ ] Test complete user workflow from station selection to results
- [ ] Verify data flows correctly between frontend and backend
- [ ] Test with real CitiBike data from Supabase
- [ ] Validate responsive design and user experience
- [ ] Performance testing for large station lists

### Phase 6: Configuration and Documentation Updates

#### Task 6.1: Railway Configuration Removal
- [ ] Remove all railway.json configuration files
- [ ] Delete Railway-specific deployment scripts
- [ ] Remove Railway CLI dependencies
- [ ] Clean up Railway environment variables
- [ ] Archive Railway-specific documentation

#### Task 6.2: Vercel + Supabase Configuration
- [ ] Create vercel.json configuration files
- [ ] Set up Supabase client configuration
- [ ] Configure build and deployment settings
- [ ] Set up environment variable management
- [ ] Create deployment automation scripts

#### Task 6.3: Documentation Updates
- [ ] Update PROJECT_PLAN.md with Vercel + Supabase architecture
- [ ] Replace old deployment guide with new deployment guides
- [ ] Update README.md with new platform information
- [ ] Update API documentation with new endpoints

#### Task 6.4: Cursor Rules Updates
- [ ] Update .cursor/rules/railway-cli-usage.mdc to Vercel/Supabase equivalents
- [ ] Update .cursor/rules/postgresql-database.mdc for Supabase specifics
- [ ] Create new rules for Vercel deployment and Supabase management
- [ ] Update test automation rules for new platform
- [ ] Remove Railway-specific rules and configurations

### Phase 7: Migration Verification and Rollback Planning

#### Task 7.1: Comprehensive Testing
- [ ] End-to-end testing of complete application
- [ ] Performance testing with real CitiBike data
- [ ] Database query performance validation
- [ ] API response time testing
- [ ] User workflow validation

#### Task 7.2: Rollback Strategy
- [ ] Keep Railway deployment running during migration
- [ ] Document rollback procedures if issues arise
- [ ] Maintain Railway data backup for emergency restoration
- [ ] Test rollback procedures before final Railway shutdown
- [ ] Plan for quick reversion if critical issues discovered

#### Task 7.3: Production Deployment
- [ ] Deploy to Vercel + Supabase production environment
- [ ] Configure custom domains if needed
- [ ] Set up monitoring and error tracking
- [ ] Verify all functionality works in production
- [ ] Monitor performance and stability

#### Task 7.4: Railway Shutdown
- [ ] Verify Vercel + Supabase deployment is stable
- [ ] Export final data backup from Railway
- [ ] Document Railway shutdown procedures
- [ ] Remove Railway project and services
- [ ] Update all external references to Railway URLs

## Migration Success Criteria

- [ ] All functionality works identically to Railway deployment
- [ ] Performance is equal to or better than Railway
- [ ] Zero data loss during migration
- [ ] Development velocity improved (no more Railway debugging)
- [ ] Reliable deployment process with Vercel + Supabase

## Risk Mitigation

### High-Risk Scenarios
1. **Data Loss During Migration**
   - **Mitigation**: Local data already available, multiple backups
   - **Rollback**: Keep Railway running until migration is verified

2. **API Endpoint Failures**
   - **Mitigation**: Comprehensive testing of all endpoints
   - **Rollback**: Maintain Railway deployment as backup

3. **Performance Degradation**
   - **Mitigation**: Performance testing with real data
   - **Rollback**: Optimize or revert if performance is unacceptable

4. **Environment Variable Issues**
   - **Mitigation**: Document all environment variables, test thoroughly
   - **Rollback**: Maintain Railway environment as reference

## Migration Timeline

**Day 1:**
- Morning: Vercel + Supabase setup and database migration
- Afternoon: Backend deployment to Vercel

**Day 2:**
- Morning: Frontend migration and integration testing
- Afternoon: Configuration cleanup and documentation updates

**Day 3 (if needed):**
- Testing, verification, and Railway shutdown

## Current Status

- [x] Migration branch created
- [x] Migration plan documented
- [x] Local data available (no backup needed)
- [ ] Vercel + Supabase setup in progress

## Next Steps

1. Set up Vercel and Supabase accounts
2. Create Supabase database and migrate local data
3. Deploy backend to Vercel
4. Deploy frontend to Vercel
5. Test complete application
6. Clean up Railway configuration
7. Document migration completion

## Data Migration Strategy

Since Railway data is already available locally:
- **Source**: Local PostgreSQL database (3.1M trips, 2,234 stations, station_mapping)
- **Target**: Supabase PostgreSQL database
- **Method**: Direct migration from local to Supabase
- **Verification**: Compare row counts and data integrity
- **Backup**: Local data serves as backup during migration