import os
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import text

# ==============================================================================
# 1. DATABASE CONNECTION CONFIGURATION (MYSQL)
# ==============================================================================
# Fetch connection details from Environment Variables.
# These variables can be easily passed when running locally or deploying to ECS.
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345678")
DB_HOST = os.getenv("DB_HOST", "lesson-11-db.c9uw0aacots3.ap-northeast-1.rds.amazonaws.com")
DB_PORT = os.getenv("DB_PORT", "3306")  # Default MySQL port is 3306
DB_NAME = os.getenv("DB_NAME", "lesson11db")

# Connection string using the 'pymysql' driver for MySQL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Initialize SQLAlchemy Engine for MySQL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==============================================================================
# 2. FASTAPI INITIALIZATION & DEPENDENCY
# ==============================================================================
app = FastAPI(title="ECS to RDS MySQL CRUD API")

# Dependency to manage opening/closing database connections per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==============================================================================
# 3. API ENDPOINTS
# ==============================================================================

@app.get("/")
async def root():
    return {"message": "This is lesson 11"}

@app.get("/helloworld")
async def helloworld():
    return {"message": "Hello World!"}

# Endpoint to check the connection status to RDS MySQL
@app.get("/ecs-rds")
async def check_rds_connection(db: Session = Depends(get_db)):
    try:
        # Execute a basic SQL statement compatible with MySQL to verify the connection
        db.execute(text("SELECT 1"))
        return {"status": "success", "message": "Successfully connected to RDS MySQL Database!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"MySQL Connection failed: {str(e)}"
        )

@app.get("/show-databases")
async def show_databases(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("show databases"))
        databases = [row[0] for row in result.fetchall()]
        return {"status": "success", "database_list": databases}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"MySQL Connection failed: {str(e)}"
        )
