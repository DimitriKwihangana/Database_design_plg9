from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from . import models, schemas
from .thedatabase import SessionLocal, engine, Base
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import List
from sqlalchemy.exc import SQLAlchemyError
import logging
from sqlalchemy import desc

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
@app.post("/water_quality/")
async def create_water_quality(water_quality_data: schemas.WaterQuality, session: AsyncSession = Depends(get_db)):
    try:
        # Create ChemicalProperties instance
        new_chemical_properties = models.ChemicalProperties(
            ph=water_quality_data.ph,
            chloramines=water_quality_data.chloramines,
            sulfate=water_quality_data.sulfate,
            conductivity=water_quality_data.conductivity,
            organic_carbon=water_quality_data.organic_carbon,
            trihalomethanes=water_quality_data.trihalomethanes
        )
        session.add(new_chemical_properties)
        await session.commit()
        await session.refresh(new_chemical_properties)

        # Create PhysicalProperties instance
        new_physical_properties = models.PhysicalProperties(
            hardness=water_quality_data.hardness,
            solids=water_quality_data.solids,
            turbidity=water_quality_data.turbidity
        )
        session.add(new_physical_properties)
        await session.commit()
        await session.refresh(new_physical_properties)

        # Create WaterQuality instance
        new_water_quality = models.WaterQuality(
            potability=water_quality_data.potability,
            chemical_properties_id=new_chemical_properties.id,
            physical_properties_id=new_physical_properties.id
        )
        session.add(new_water_quality)
        await session.commit()
        await session.refresh(new_water_quality)

        return {"id": new_water_quality.id}
    except IntegrityError as e:
        await session.rollback()
        logging.error(f"IntegrityError: {e}")
        raise HTTPException(status_code=500, detail="Error adding new water quality data")
    except Exception as e:
        await session.rollback()
        logging.error(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")



@app.get("/water_quality/{water_quality_id}", response_model=schemas.WaterQuality)
async def get_water_quality(water_quality_id: int, session: AsyncSession = Depends(get_db)):
    # Query the WaterQuality with joined ChemicalProperties and PhysicalProperties
    result = await session.execute(
        select(models.WaterQuality)
        .filter(models.WaterQuality.id == water_quality_id)
        .options(
            joinedload(models.WaterQuality.chemical_properties),
            joinedload(models.WaterQuality.physical_properties)
        )
    )
    water_quality = result.scalars().first()

    if not water_quality:
        raise HTTPException(status_code=404, detail="Water quality data not found")

    # Return the response using the existing Pydantic schema (WaterQuality)
    return schemas.WaterQuality(
        potability=water_quality.potability,
        ph=water_quality.chemical_properties.ph,
        chloramines=water_quality.chemical_properties.chloramines,
        sulfate=water_quality.chemical_properties.sulfate,
        conductivity=water_quality.chemical_properties.conductivity,
        organic_carbon=water_quality.chemical_properties.organic_carbon,
        trihalomethanes=water_quality.chemical_properties.trihalomethanes,
        hardness=water_quality.physical_properties.hardness,
        solids=water_quality.physical_properties.solids,
        turbidity=water_quality.physical_properties.turbidity
    )

@app.put("/water_quality/{water_quality_id}", response_model=schemas.WaterQuality)
async def update_water_quality(
    water_quality_id: int,
    water_quality_data: schemas.WaterQuality,
    session: AsyncSession = Depends(get_db)
):
    # Query the WaterQuality record
    result = await session.execute(
        select(models.WaterQuality)
        .filter(models.WaterQuality.id == water_quality_id)
        .options(
            joinedload(models.WaterQuality.chemical_properties),
            joinedload(models.WaterQuality.physical_properties)
        )
    )
    water_quality = result.scalars().first()

    if not water_quality:
        raise HTTPException(status_code=404, detail="Water quality data not found")

    # Update the water quality data (assuming the user is updating full data)
    water_quality.potability = water_quality_data.potability
    water_quality.chemical_properties.ph = water_quality_data.ph
    water_quality.chemical_properties.chloramines = water_quality_data.chloramines
    water_quality.chemical_properties.sulfate = water_quality_data.sulfate
    water_quality.chemical_properties.conductivity = water_quality_data.conductivity
    water_quality.chemical_properties.organic_carbon = water_quality_data.organic_carbon
    water_quality.chemical_properties.trihalomethanes = water_quality_data.trihalomethanes
    water_quality.physical_properties.hardness = water_quality_data.hardness
    water_quality.physical_properties.solids = water_quality_data.solids
    water_quality.physical_properties.turbidity = water_quality_data.turbidity

    # Commit the changes to the database
    await session.commit()
    await session.refresh(water_quality)

    return schemas.WaterQuality(
        potability=water_quality.potability,
        ph=water_quality.chemical_properties.ph,
        chloramines=water_quality.chemical_properties.chloramines,
        sulfate=water_quality.chemical_properties.sulfate,
        conductivity=water_quality.chemical_properties.conductivity,
        organic_carbon=water_quality.chemical_properties.organic_carbon,
        trihalomethanes=water_quality.chemical_properties.trihalomethanes,
        hardness=water_quality.physical_properties.hardness,
        solids=water_quality.physical_properties.solids,
        turbidity=water_quality.physical_properties.turbidity
    )


@app.get("/water_quality/", response_model=List[schemas.WaterQuality])
async def get_all_water_quality(session: AsyncSession = Depends(get_db)):
    try:
        # Query all water quality records with their associated chemical and physical properties
        result = await session.execute(
            select(models.WaterQuality)
            .options(
                joinedload(models.WaterQuality.chemical_properties),
                joinedload(models.WaterQuality.physical_properties)
            )
        )
        water_quality_data = result.scalars().all()

        if not water_quality_data:
            raise HTTPException(status_code=404, detail="No water quality data found")

        # Return the data as a list of Pydantic models
        return [
            schemas.WaterQuality(
                potability=water_quality.potability,
                ph=water_quality.chemical_properties.ph,
                chloramines=water_quality.chemical_properties.chloramines,
                sulfate=water_quality.chemical_properties.sulfate,
                conductivity=water_quality.chemical_properties.conductivity,
                organic_carbon=water_quality.chemical_properties.organic_carbon,
                trihalomethanes=water_quality.chemical_properties.trihalomethanes,
                hardness=water_quality.physical_properties.hardness,
                solids=water_quality.physical_properties.solids,
                turbidity=water_quality.physical_properties.turbidity
            )
            for water_quality in water_quality_data
        ]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to delete a row by ID
@app.delete("/water_quality/{water_quality_id}/")
async def delete_water_quality(water_quality_id: int, db: AsyncSession = Depends(get_db)):
    try:
        # Query the WaterQuality record with the associated child records (ChemicalProperties and PhysicalProperties)
        result = await db.execute(
            select(models.WaterQuality)
            .filter(models.WaterQuality.id == water_quality_id)
            .options(
                joinedload(models.WaterQuality.chemical_properties),
                joinedload(models.WaterQuality.physical_properties)
            )
        )
        water_quality = result.scalars().first()

        if not water_quality:
            raise HTTPException(status_code=404, detail="Water quality data not found")

        # Delete related child records first
        await db.delete(water_quality.chemical_properties)
        await db.delete(water_quality.physical_properties)

        # Then delete the parent record (WaterQuality)
        await db.delete(water_quality)
        
        await db.commit()

        return {"message": "Water quality data and related records deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()  # Ensure rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))

