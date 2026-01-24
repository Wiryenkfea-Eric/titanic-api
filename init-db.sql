-- Initialize Titanic Database
-- This script runs automatically when the database container starts

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE titanic_db TO titanic_user;

-- Note: Application migrations will create tables
-- This file is for initial setup only
