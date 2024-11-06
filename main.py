from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from databases import Database
from pydantic import BaseModel

app = FastAPI()

# Database URL with async support for SQLAlchemy
DATABASE_URL = "postgresql+asyncpg://root:vs1kol6cpH9KmVe0U8hVuO52sdwv2MeF@dpg-csl7uqe8ii6s73c181ag-a.oregon-postgres.render.com/customer_database_5rln"

# Setup async SQLAlchemy engine and session
async_engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

# Setup database connection with 'databases' package
database = Database(DATABASE_URL)

# Define base for SQLAlchemy ORM
Base = declarative_base()

# Define Customer ORM model
class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255))

# Create all tables in the database (this is needed to create 'customers' table)
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Pydantic model for request validation
class CustomerCreate(BaseModel):
    name: str

@app.on_event("startup")
async def on_startup():
    await database.connect()
    await init_db()

@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()



# API to get all customers
@app.get("/customers")
async def read_customers():
    async with SessionLocal() as session:
        result = await session.execute(select(Customer))
        customers = result.scalars().all()
        return [{"id": customer.customer_id, "first_name": customer.first_name} for customer in customers]
