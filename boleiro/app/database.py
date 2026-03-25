# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# SQLite para desenvolvimento — troque pela URL do PostgreSQL em produção:
# DATABASE_URL = "postgresql://usuario:senha@localhost/boleiro"
DATABASE_URL = "sqlite:///./boleiro.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # só necessário para SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    """Dependency: abre e fecha a sessão do banco automaticamente."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
