#!/usr/bin/env python3
"""
CitiBike Application Startup Script
Handles complete local development environment setup and launch
"""

import os
import sys
import time
import subprocess
import requests
import signal
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('startup.log')
    ]
)
logger = logging.getLogger(__name__)

class CitiBikeAppStarter:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent  # Go up 3 levels: utils/deployment_scripts/ -> utils/ -> project_root
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        
        # Service status
        self.backend_process = None
        self.frontend_process = None
        self.services_running = False
        
        # Configuration
        self.backend_port = 8000
        self.frontend_port = 3000
        self.backend_url = f"http://localhost:{self.backend_port}"
        self.frontend_url = f"http://localhost:{self.frontend_port}"
        
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met"""
        logger.info("🔍 Checking prerequisites...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            logger.error(f"❌ Python 3.8+ required, found {python_version.major}.{python_version.minor}")
            return False
        logger.info(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check Node.js
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"✅ Node.js {result.stdout.strip()}")
            else:
                logger.error("❌ Node.js not found")
                return False
        except FileNotFoundError:
            logger.error("❌ Node.js not found")
            return False
        
        # Check directories exist
        required_dirs = [self.backend_dir, self.frontend_dir]
        for dir_path in required_dirs:
            if not dir_path.exists():
                logger.error(f"❌ Directory not found: {dir_path}")
                return False
            logger.info(f"✅ Directory exists: {dir_path}")
        
        return True
    
    def setup_database(self) -> bool:
        """Set up database with real CitiBike data"""
        logger.info("🗄️ Setting up database...")
        
        # Check if database exists and has real data
        db_path = self.project_root / "dev.db"
        if db_path.exists():
            try:
                import sqlite3
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Check if we have real data
                cursor.execute("SELECT COUNT(*) FROM stations")
                station_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM trips")
                trip_count = cursor.fetchone()[0]
                
                conn.close()
                
                if station_count > 100 and trip_count > 100000:
                    logger.info(f"✅ Database has real data ({station_count} stations, {trip_count} trips)")
                    return True
                else:
                    logger.info("🔄 Database has sample data, loading real data...")
            except Exception as e:
                logger.warning(f"⚠️ Could not check database: {e}")
        
        # Load real data
        try:
            result = subprocess.run(
                [sys.executable, '../utils/data_processing/load_real_data.py'],
                cwd=self.backend_dir,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                logger.info("✅ Real CitiBike data loaded into database")
                return True
            else:
                logger.error(f"❌ Failed to load real data: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"❌ Error loading real data: {e}")
            return False
    
    def start_backend(self) -> bool:
        """Start the FastAPI backend server"""
        logger.info("🚀 Starting backend server...")
        
        try:
            # Start backend in background
            self.backend_process = subprocess.Popen(
                [sys.executable, 'main.py'],
                cwd=self.backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for backend to start
            for attempt in range(30):  # Wait up to 30 seconds
                try:
                    response = requests.get(f"{self.backend_url}/api/health", timeout=2)
                    if response.status_code == 200:
                        logger.info(f"✅ Backend server running on {self.backend_url}")
                        return True
                except requests.exceptions.RequestException:
                    pass
                
                time.sleep(1)
            
            logger.error("❌ Backend server failed to start")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error starting backend: {e}")
            return False
    
    def start_frontend(self) -> bool:
        """Start the Next.js frontend server"""
        logger.info("🚀 Starting frontend server...")
        
        try:
            # Start frontend in background
            self.frontend_process = subprocess.Popen(
                ['npm', 'run', 'dev'],
                cwd=self.frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for frontend to start
            for attempt in range(60):  # Wait up to 60 seconds
                try:
                    response = requests.get(self.frontend_url, timeout=2)
                    if response.status_code == 200:
                        logger.info(f"✅ Frontend server running on {self.frontend_url}")
                        return True
                except requests.exceptions.RequestException:
                    pass
                
                time.sleep(1)
            
            logger.error("❌ Frontend server failed to start")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error starting frontend: {e}")
            return False
    
    def test_integration(self) -> bool:
        """Test integration between frontend and backend"""
        logger.info("🔗 Testing integration...")
        
        # Give the backend a moment to fully initialize
        time.sleep(3)
        
        try:
            # Test stations endpoint with longer timeout
            response = requests.get(f"{self.backend_url}/api/stations", timeout=30)
            if response.status_code == 200:
                stations = response.json()
                logger.info(f"✅ Stations API working ({len(stations)} stations)")
            else:
                logger.warning(f"⚠️ Stations API returned status {response.status_code}")
                return False
            
            # Test frontend can reach backend with longer timeout
            response = requests.get(f"{self.frontend_url}/api/stations", timeout=30)
            if response.status_code == 200:
                logger.info("✅ Frontend-backend integration working")
            else:
                logger.warning(f"⚠️ Frontend-backend integration returned status {response.status_code}")
                return False
            
            return True
            
        except requests.exceptions.Timeout as e:
            logger.warning(f"⚠️ Integration test timed out: {e}")
            return False
        except Exception as e:
            logger.warning(f"⚠️ Integration test failed: {e}")
            return False
    
    def show_status(self):
        """Show application status and useful information"""
        logger.info("\n" + "="*60)
        logger.info("🎉 CitiBike Application Started Successfully!")
        logger.info("="*60)
        logger.info(f"📱 Frontend: {self.frontend_url}")
        logger.info(f"🔧 Backend API: {self.backend_url}")
        logger.info(f"📊 API Health: {self.backend_url}/api/health")
        logger.info(f"🏪 Stations API: {self.backend_url}/api/stations")
        logger.info("="*60)
        logger.info("💡 Tips:")
        logger.info("  - Open the frontend URL in your browser")
        logger.info("  - Use Ctrl+C to stop all services")
        logger.info("  - Check startup.log for detailed logs")
        logger.info("="*60)
    
    def cleanup(self):
        """Clean up processes on shutdown"""
        logger.info("🧹 Cleaning up...")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            self.frontend_process.wait()
            logger.info("✅ Frontend stopped")
        
        if self.backend_process:
            self.backend_process.terminate()
            self.backend_process.wait()
            logger.info("✅ Backend stopped")
    
    def run(self):
        """Main startup sequence"""
        try:
            logger.info("🚀 Starting CitiBike Application...")
            
            # Step 1: Check prerequisites
            if not self.check_prerequisites():
                logger.error("❌ Prerequisites check failed")
                return False
            
            # Step 2: Setup database
            if not self.setup_database():
                logger.error("❌ Database setup failed")
                return False
            
            # Step 3: Start backend
            if not self.start_backend():
                logger.error("❌ Backend startup failed")
                return False
            
            # Step 4: Start frontend
            if not self.start_frontend():
                logger.error("❌ Frontend startup failed")
                return False
            
            # Step 5: Test integration (non-blocking)
            integration_success = self.test_integration()
            if not integration_success:
                logger.warning("⚠️ Integration test failed, but continuing with startup...")
            
            # Step 6: Show status
            self.show_status()
            
            self.services_running = True
            
            # Keep running until interrupted
            try:
                while self.services_running:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("\n🛑 Shutdown requested...")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Startup failed: {e}")
            return False
        finally:
            self.cleanup()

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"\n🛑 Received signal {signum}, shutting down...")
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run the starter
    starter = CitiBikeAppStarter()
    success = starter.run()
    
    if success:
        logger.info("✅ Application started successfully")
    else:
        logger.error("❌ Application startup failed")
        sys.exit(1)
