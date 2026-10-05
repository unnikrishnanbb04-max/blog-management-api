from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# DATABASE_URL = "sqlite:///./blog.db"
DATABASE_URL = "mysql+pymysql://root:Sureshjeya%40123@localhost:3306/blogapi"

engine = create_engine(
    DATABASE_URL,
    # connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()