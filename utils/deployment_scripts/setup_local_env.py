#!/usr/bin/env python3
"""
Local Environment Setup Script

This script helps set up the local environment for PostgreSQL development.
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_env_file():
    """Create .env file for local development"""
    env_content = """# Local Development Database Configuration
DATABASE_URL=postgresql://postgres@localhost:5432/citibike_dev

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Environment
ENVIRONMENT=development

# CORS Settings (for local development)
CORS_ORIGINS=["http://localhost:3000"]

# Logging
LOG_LEVEL=INFO
"""
    
    env_file_path = ".env"
    
    if os.path.exists(env_file_path):
        logger.info("✅ .env file already exists")
        return True
    
    try:
        with open(env_file_path, 'w') as f:
            f.write(env_content)
        logger.info("✅ Created .env file for local development")
        logger.info("💡 DATABASE_URL set to: postgresql://postgres@localhost:5432/citibike_dev")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create .env file: {e}")
        return False

def print_setup_instructions():
    """Print setup instructions for the user"""
    logger.info("=" * 60)
    logger.info("🚀 PostgreSQL Migration Setup Instructions")
    logger.info("=" * 60)
    logger.info("")
    logger.info("1. Install PostgreSQL (if not already installed):")
    logger.info("   macOS: brew install postgresql")
    logger.info("   Ubuntu: sudo apt-get install postgresql postgresql-contrib")
    logger.info("   Windows: Download from https://www.postgresql.org/download/windows/")
    logger.info("")
    logger.info("2. Start PostgreSQL service:")
    logger.info("   macOS: brew services start postgresql")
    logger.info("   Ubuntu: sudo systemctl start postgresql")
    logger.info("")
    logger.info("3. Run the PostgreSQL setup script:")
    logger.info("   python setup_local_postgres.py")
    logger.info("")
    logger.info("4. If you have existing SQLite data, migrate it:")
    logger.info("   python migrate_data_to_postgres.py")
    logger.info("")
    logger.info("5. Test the application:")
    logger.info("   python main.py")
    logger.info("")
    logger.info("6. Run database migrations (if needed):")
    logger.info("   alembic upgrade head")
    logger.info("")
    logger.info("💡 The application will now use PostgreSQL locally!")
    logger.info("💡 This matches the production Railway environment.")
    logger.info("")

def main():
    """Main setup function"""
    logger.info("🔧 Setting up local environment for PostgreSQL development...")
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Print instructions
    print_setup_instructions()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 