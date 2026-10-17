import os
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
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
# 2. ORM MODEL DEFINITION (Database Table)
# ==============================================================================
class DBItem(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    # NOTE: In MySQL, indexed String columns must have a specified length (e.g., VARCHAR(100))
    title = Column(String(100), index=True, nullable=False)
    description = Column(String(255), nullable=True)

# Automatically create tables in MySQL if they do not exist
Base.metadata.create_all(bind=engine)


# ==============================================================================
# 3. PYDANTIC SCHEMAS (API Request/Response Data Validation)
# ==============================================================================
class ItemBase(BaseModel):
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True


# ==============================================================================
# 4. FASTAPI INITIALIZATION & DEPENDENCY
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
# 5. API ENDPOINTS
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

# --- CRUD FUNCTIONS ---

# CREATE: Add a new record
@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = DBItem(title=item.title, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# READ ALL: Fetch a list of records (with pagination)
@app.get("/items", response_model=list[ItemResponse])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(DBItem).offset(skip).limit(limit).all()
    return items

# READ ONE: Fetch a single record details by ID
@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# UPDATE: Modify an existing record by ID
@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, updated_item: ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item.title = updated_item.title
    db_item.description = updated_item.description
    db.commit()
    db.refresh(db_item)
    return db_item

# DELETE: Remove a record by ID
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return None
