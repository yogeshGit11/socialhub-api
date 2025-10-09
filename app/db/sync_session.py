from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

sync_db_url = settings.DATABASE_URL.replace("sqlite+aiosqlite", "sqlite")
sync_engine = create_engine(sync_db_url, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
