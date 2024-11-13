
# app/thedatabase.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://root:vs1kol6cpH9KmVe0U8hVuO52sdwv2MeF@dpg-csl7uqe8ii6s73c181ag-a.oregon-postgres.render.com/customer_database_5rln"

# Create the asynchronous engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()
