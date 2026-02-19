# this is to connect to the db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# CHANGE THIS to your password and db name!
# Format: postgresql://username:password@localhost/dbname
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password123@localhost/nlp_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency (This helps you get the DB session in your endpoints)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()