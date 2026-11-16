from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base, sessionmaker



DATABASE_URL = ("postgresql+psycopg://postgres:mc_c13370r"
                "@localhost:5432/to-Do_db"
)


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base = declarative_base()
