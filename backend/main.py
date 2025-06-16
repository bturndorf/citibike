from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import List, Optional
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from prob_calc import calculate_probability

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CitiBike Rider Probability API",
    description="API for calculating CitiBike rider encounter probabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    message: str
    version: str

class Station(BaseModel):
    id: int
    station_id: str
    name: str
    latitude: float
    longitude: float
    total_trips: Optional[int] = None
    unique_bikes: Optional[int] = None

class ProbabilityRequest(BaseModel):
    home_station_id: str
    riding_frequency: int  # rides per week
    time_pattern: str  # "weekday", "weekend", "both"
    date_range: Optional[str] = None

class ProbabilityResponse(BaseModel):
    probability: float
    confidence_interval: str
    explanation: str
    station_info: Optional[dict] = None

# Load environment variables from .env
load_dotenv()

# Use test database if TESTING environment variable is set
if os.getenv("TESTING") == "true":
    DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://localhost:5432/citibike_test")
    logger.info("Using test database for testing mode")
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/citibike_dev")
    logger.info("Using production database")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def ensure_database_indexes():
    """Ensure all required database indexes exist for optimal performance"""
    try:
        with engine.connect() as conn:
            # Check if indexes exist
            index_check_query = text("""
                SELECT indexname 
                FROM pg_indexes 
                WHERE tablename IN ('trips', 'station_mapping')
                AND indexname IN (
                    'idx_trips_station_time',
                    'idx_trips_bike_end_time', 
                    'idx_trips_end_station_time',
                    'idx_station_mapping_uuid',
                    'idx_station_mapping_name'
                )
            """)
            
            result = conn.execute(index_check_query)
            existing_indexes = {row.indexname for row in result}
            
            required_indexes = {
                'idx_trips_station_time',
                'idx_trips_bike_end_time',
                'idx_trips_end_station_time', 
                'idx_station_mapping_uuid',
                'idx_station_mapping_name'
            }
            
            missing_indexes = required_indexes - existing_indexes
            
            if missing_indexes:
                logger.warning(f"Missing indexes: {missing_indexes}")
                logger.warning("Please run database migrations: alembic upgrade head")
                logger.warning("Or set AUTO_CREATE_INDEXES=true to create them automatically")
                
                # Auto-create indexes if environment variable is set
                if os.getenv("AUTO_CREATE_INDEXES", "false").lower() == "true":
                    logger.info("Auto-creating missing indexes...")
                    create_missing_indexes(conn, missing_indexes)
                else:
                    logger.warning("Indexes missing but auto-creation disabled")
            else:
                logger.info("All required database indexes are present")
                
    except Exception as e:
        logger.error(f"Error checking database indexes: {e}")

def create_missing_indexes(conn, missing_indexes):
    """Create missing indexes for performance optimization"""
    index_definitions = {
        'idx_trips_station_time': """
            CREATE INDEX IF NOT EXISTS idx_trips_station_time 
            ON trips(start_station_id, started_at)
        """,
        'idx_trips_bike_end_time': """
            CREATE INDEX IF NOT EXISTS idx_trips_bike_end_time 
            ON trips(bike_id, end_station_id, started_at)
        """,
        'idx_trips_end_station_time': """
            CREATE INDEX IF NOT EXISTS idx_trips_end_station_time 
            ON trips(end_station_id, started_at)
        """,
        'idx_station_mapping_uuid': """
            CREATE INDEX IF NOT EXISTS idx_station_mapping_uuid 
            ON station_mapping(uuid_station_id)
        """,
        'idx_station_mapping_name': """
            CREATE INDEX IF NOT EXISTS idx_station_mapping_name 
            ON station_mapping(station_name)
        """
    }
    
    for index_name in missing_indexes:
        if index_name in index_definitions:
            try:
                conn.execute(text(index_definitions[index_name]))
                logger.info(f"Created index: {index_name}")
            except Exception as e:
                logger.error(f"Failed to create index {index_name}: {e}")

# Test DB connection on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database connection and ensure indexes on startup"""
    try:
        with engine.connect() as conn:
            logger.info("Database connection successful.")
        
        # Ensure database indexes exist
        ensure_database_indexes()
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

# Health check endpoint
@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for Railway deployment"""
    return HealthResponse(
        status="healthy",
        message="CitiBike Probability API is running",
        version="1.0.0"
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with basic information"""
    return {
        "message": "CitiBike Rider Probability API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "stations": "/api/stations",
            "probability": "/api/probability"
        }
    }

# Stations endpoint with real database query
@app.get("/api/stations", response_model=List[Station])
async def get_stations(db: Session = Depends(get_db)):
    """Get list of all CitiBike stations with statistics"""
    try:
        # Query stations with trip statistics using station_mapping table
        query = text("""
            SELECT 
                s.id,
                s.station_id,
                s.name,
                s.latitude,
                s.longitude,
                COUNT(t.id) as total_trips,
                COUNT(DISTINCT t.bike_id) as unique_bikes
            FROM stations s
            LEFT JOIN station_mapping sm ON s.station_id = sm.uuid_station_id
            LEFT JOIN trips t ON sm.numeric_station_id = t.start_station_id
            GROUP BY s.id, s.station_id, s.name, s.latitude, s.longitude
            ORDER BY total_trips DESC
        """)
        
        result = db.execute(query)
        stations = []
        
        for row in result:
            stations.append(Station(
                id=row.id,
                station_id=row.station_id,
                name=row.name,
                latitude=float(row.latitude),
                longitude=float(row.longitude),
                total_trips=row.total_trips or 0,
                unique_bikes=row.unique_bikes or 0
            ))
        
        logger.info(f"Retrieved {len(stations)} stations")
        return stations
        
    except Exception as e:
        logger.error(f"Error retrieving stations: {e}")
        # Fallback to basic station list if query fails
        return [
            Station(
                id=1,
                station_id="test_station_1",
                name="Test Station 1",
                latitude=40.7589,
                longitude=-73.9851,
                total_trips=0,
                unique_bikes=0
            )
        ]

# Probability calculation endpoint with real implementation
@app.post("/api/probability", response_model=ProbabilityResponse)
async def calculate_probability_endpoint(request: ProbabilityRequest, db: Session = Depends(get_db)):
    """Calculate probability of encountering the same bike twice"""
    try:
        logger.info(f"Probability calculation requested")
        logger.info(f"Request parameters: station_id={request.home_station_id}, frequency={request.riding_frequency}, pattern={request.time_pattern}")
        
        # Use the probability calculation module
        logger.info("Calling calculate_probability function")
        result = calculate_probability(
            db_session=db,
            home_station_id=request.home_station_id,
            riding_frequency=request.riding_frequency,
            time_pattern=request.time_pattern
        )
        
        logger.info(f"Probability calculation completed successfully: {result}")
        
        return ProbabilityResponse(
            probability=result['probability'],
            confidence_interval=result['confidence_interval'],
            explanation=result['explanation'],
            station_info=result.get('station_info')
        )
        
    except ValueError as e:
        logger.error(f"Invalid request: {e}")
        logger.error(f"Request parameters that caused error: station_id={request.home_station_id}, frequency={request.riding_frequency}, pattern={request.time_pattern}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error calculating probability: {e}")
        logger.error(f"Exception type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error during probability calculation")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 