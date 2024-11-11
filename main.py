from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, String, Integer, Boolean,ForeignKey, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from databases import Database
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from routes.route import router
from fastapi import Depends 
from sqlalchemy.orm import relationship
from typing import Optional,Dict,List

app = FastAPI()

# Database URL with async support for SQLAlchemy
DATABASE_URL = "postgresql+asyncpg://root:vs1kol6cpH9KmVe0U8hVuO52sdwv2MeF@dpg-csl7uqe8ii6s73c181ag-a.oregon-postgres.render.com/customer_database_5rln"

app.include_router(router)


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

# class WaterQuality(Base):
#     __tablename__ = 'water_quality'
#     sample_id = Column(Integer, primary_key=True, autoincrement=True)
#     potability = Column(Boolean)

####### Other table ORM models
# Create all tables in the database (this is needed to create 'customers' table)

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

# async def init_db():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# # Pydantic model for request validation
# class CustomerCreate(BaseModel):
#     name: str

# @app.on_event("startup")
# async def on_startup():
#     await database.connect()
#     await init_db()

# @app.on_event("shutdown")
# async def on_shutdown():
#     await database.disconnect()



# # API to get all customers
# @app.get("/customers")
# async def read_customers():
#     async with SessionLocal() as session:
#         result = await session.execute(select(Customer))
#         customers = result.scalars().all()
#         return [{"id": customer.customer_id, "first_name": customer.first_name} for customer in customers]


class WaterQuality(Base):
    __tablename__ = 'water_quality'
    __table_args__ = {'extend_existing': True} 
    sample_id = Column(Integer, primary_key=True, autoincrement=True)
    potability = Column(Boolean)
    chemical_properties = relationship("ChemicalProperties", back_populates="water_quality", cascade="all, delete")
    physical_properties = relationship("PhysicalProperties", back_populates="water_quality",cascade="all, delete")

class WaterQualityCreate(BaseModel):
    potability: bool

class WaterQualityResponse(BaseModel):
    sample_id: int
    potability: bool

class WaterQualityUpdate(BaseModel):
    potability: bool

@app.post("sql/water-quality", response_model=WaterQualityResponse)
async def create_water_quality(water_quality: WaterQualityCreate, session: AsyncSession = Depends(get_session)):
    new_sample = WaterQuality(potability=water_quality.potability)
    session.add(new_sample)
    await session.commit()
    await session.refresh(new_sample)
    return WaterQualityResponse(sample_id=new_sample.sample_id, potability=new_sample.potability)

# Get a water quality sample by ID
@app.get("/sql/water-quality/{sample_id}", response_model=WaterQualityResponse)
async def get_water_quality(sample_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(WaterQuality).where(WaterQuality.sample_id == sample_id))
    water_quality = result.scalars().first()
    if not water_quality:
        raise HTTPException(status_code=404, detail="Sample not found")
    return WaterQualityResponse(sample_id=water_quality.sample_id, potability=water_quality.potability)

# Update a water quality sample
@app.put("/sql/water-quality/{sample_id}", response_model=WaterQualityResponse)
async def update_water_quality(sample_id: int, water_quality: WaterQualityUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(WaterQuality).where(WaterQuality.sample_id == sample_id))
    existing_sample = result.scalars().first()
    if not existing_sample:
        raise HTTPException(status_code=404, detail="Sample not found")

    await session.execute(
        update(WaterQuality)
        .where(WaterQuality.sample_id == sample_id)
        .values(potability=water_quality.potability)
    )
    await session.commit()
    await session.refresh(existing_sample)
    return WaterQualityResponse(sample_id=existing_sample.sample_id, potability=existing_sample.potability)

# Delete a water quality sample
@app.delete("/sql/water-quality/{sample_id}", status_code=204)
async def delete_water_quality(sample_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(WaterQuality).where(WaterQuality.sample_id == sample_id))
    water_quality = result.scalars().first()
    if not water_quality:
        raise HTTPException(status_code=404, detail="Sample not found")

    await session.execute(delete(WaterQuality).where(WaterQuality.sample_id == sample_id))
    await session.commit()
    return None

# Get all water quality samples
@app.get("/sql/water-quality", response_model=list[WaterQualityResponse])
async def get_all_water_quality_samples(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(WaterQuality))
    samples = result.scalars().all()
    return [WaterQualityResponse(sample_id=sample.sample_id, potability=sample.potability) for sample in samples]


#######

# Define the ChemicalProperties model
class ChemicalProperties(Base):
    __tablename__ = 'chemical_properties'
    __table_args__ = {'extend_existing': True}  # Allow redefinition if the table already exists

    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_id = Column(Integer, ForeignKey('water_quality.sample_id'))
    ph = Column(Float)
    chloramines = Column(Float)
    sulfate = Column(Float)
    conductivity = Column(Float)
    organic_carbon = Column(Float)
    trihalomethanes = Column(Float)

    # Use string 'WaterQuality' to defer resolution of the relationship
    water_quality = relationship("WaterQuality", back_populates="chemical_properties")

# class WaterQuality(Base):
#     __tablename__ = 'water_quality'
#     __table_args__ = {'extend_existing': True}

#     sample_id = Column(Integer, primary_key=True, autoincrement=True)
#     potability = Column(Boolean)
#     chemical_properties = relationship("ChemicalProperties", back_populates="water_quality", cascade="all, delete")


# Pydantic models
class ChemicalPropertiesCreate(BaseModel):
    sample_id: int
    ph: float
    chloramines: float
    sulfate: float
    conductivity: float
    organic_carbon: float
    trihalomethanes: float

class ChemicalPropertiesResponse(BaseModel):
    id: int
    sample_id: int
    ph: float
    chloramines: float
    sulfate: float
    conductivity: float
    organic_carbon: float
    trihalomethanes: float

class ChemicalPropertiesUpdate(BaseModel):
    ph: Optional[float] = None
    chloramines: Optional[float] = None
    sulfate: Optional[float] = None
    conductivity: Optional[float] = None
    organic_carbon: Optional[float] = None
    trihalomethanes: Optional[float] = None

# CRUD endpoints

# Create a new chemical properties entry
@app.post("/sql/chemical-properties", response_model=ChemicalPropertiesResponse)
async def create_chemical_properties(properties: ChemicalPropertiesCreate, session: AsyncSession = Depends(get_session)):
    new_properties = ChemicalProperties(**properties.dict())
    session.add(new_properties)
    await session.commit()
    await session.refresh(new_properties)
    return new_properties

# Get a chemical properties entry by ID
@app.get("/sql/chemical-properties/{id}", response_model=ChemicalPropertiesResponse)
async def get_chemical_properties(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ChemicalProperties).where(ChemicalProperties.id == id))
    properties = result.scalars().first()
    if not properties:
        raise HTTPException(status_code=404, detail="Chemical properties not found")
    return properties

# Update a chemical properties entry
@app.put("/sql/chemical-properties/{id}", response_model=ChemicalPropertiesResponse)
async def update_chemical_properties(id: int, properties: ChemicalPropertiesUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ChemicalProperties).where(ChemicalProperties.id == id))
    existing_properties = result.scalars().first()
    if not existing_properties:
        raise HTTPException(status_code=404, detail="Chemical properties not found")

    for field, value in properties.dict(exclude_unset=True).items():
        setattr(existing_properties, field, value)

    await session.commit()
    await session.refresh(existing_properties)
    return existing_properties

# Delete a chemical properties entry
@app.delete("/sql/chemical-properties/{id}", status_code=204)
async def delete_chemical_properties(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ChemicalProperties).where(ChemicalProperties.id == id))
    properties = result.scalars().first()
    if not properties:
        raise HTTPException(status_code=404, detail="Chemical properties not found")

    await session.delete(properties)
    await session.commit()
    return None

# Get all chemical properties entries for a specific water sample
@app.get("/sql/water-quality/{sample_id}/chemical-properties", response_model=list[ChemicalPropertiesResponse])
async def get_properties_by_sample_id(sample_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ChemicalProperties).where(ChemicalProperties.sample_id == sample_id))
    properties = result.scalars().all()
    return properties

class PhysicalProperties(Base):
    __tablename__ = 'physical_properties'
    __table_args__ = {'extend_existing': True}  # Allow redefinition if the table already exists

    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_id = Column(Integer, ForeignKey('water_quality.sample_id'))
    hardness = Column(Float)
    solids = Column(Float)
    turbidity = Column(Float)

    # Use string 'WaterQuality' to defer resolution of the relationship
    water_quality = relationship("WaterQuality", back_populates="physical_properties")


class PhysicalPropertiesCreate(BaseModel):
    sample_id: int
    hardness: float
    solids: float
    turbidity: float

class PhysicalPropertiesResponse(BaseModel):
    id: int
    sample_id: int
    hardness: float
    solids: float
    turbidity: float

class PhysicalPropertiesUpdate(BaseModel):
    hardness: Optional[float] = None
    solids: Optional[float] = None
    turbidity: Optional[float] = None
 

@app.post("/sql/physical-properties", response_model=PhysicalPropertiesResponse)
async def create_physical_properties(properties: PhysicalPropertiesCreate, session: AsyncSession = Depends(get_session)):
    new_properties = PhysicalProperties(**properties.dict())
    session.add(new_properties)
    await session.commit()
    await session.refresh(new_properties)
    return new_properties

# Get a physical properties entry by ID
@app.get("/sql/physical-properties/{id}", response_model=PhysicalPropertiesResponse)
async def get_physical_properties(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(PhysicalProperties).where(PhysicalProperties.id == id))
    properties = result.scalars().first()
    if not properties:
        raise HTTPException(status_code=404, detail="Physical properties not found")
    return properties

# Update a physical properties entry
@app.put("/sql/physical-properties/{id}", response_model=PhysicalPropertiesResponse)
async def update_physical_properties(id: int, properties: PhysicalPropertiesUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(PhysicalProperties).where(PhysicalProperties.id == id))
    existing_properties = result.scalars().first()
    if not existing_properties:
        raise HTTPException(status_code=404, detail="Physical properties not found")

    for field, value in properties.dict(exclude_unset=True).items():
        setattr(existing_properties, field, value)

    await session.commit()
    await session.refresh(existing_properties)
    return existing_properties

# Delete a physical properties entry
@app.delete("/sql/physical-properties/{id}", status_code=204)
async def delete_physical_properties(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(PhysicalProperties).where(PhysicalProperties.id == id))
    properties = result.scalars().first()
    if not properties:
        raise HTTPException(status_code=404, detail="Physical properties not found")

    await session.delete(properties)
    await session.commit()
    return None

# Get all physical properties entries for a specific water sample
@app.get("/sql/water-quality/{sample_id}/physical-properties", response_model=list[PhysicalPropertiesResponse])
async def get_physical_properties_by_sample_id(sample_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(PhysicalProperties).where(PhysicalProperties.sample_id == sample_id))
    properties = result.scalars().all()
    return properties


