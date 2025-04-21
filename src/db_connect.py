from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Database Connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./patient_vitals.db"  # SQLite file
# For PostgreSQL: "postgresql://user:password@localhost/dbname"

# 2. Engine Setup
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite-specific
)

# 3. Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base Class for Models
Base = declarative_base()
