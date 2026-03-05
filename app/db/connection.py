# this is to connect to the db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Import your settings object from wherever you saved it
from app.config.setting import settings

# 2. Create the engine using the URL validated by Pydantic
engine = create_engine(settings.DATABASE_URL.get_secret_value())

# 3. Create the session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the Base class
Base = declarative_base()

# 5. Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()