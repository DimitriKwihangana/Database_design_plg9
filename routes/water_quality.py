# routes/water_quality.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from thedatabase import get_db  # Import get_db from thedatabase module
from model import WaterQuality, ChemicalProperties, PhysicalProperties
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from schema.sqlschema import CreateSampleRequestSchema, WaterQualityResponseSchema
import random

# Create a new router instance
router = APIRouter()

# Define the route within the router
@router.get("/sample/{sample_id}")
async def get_water_quality(sample_id: int, db: AsyncSession = Depends(get_db)):
    # Query for the main water quality sample
    result = await db.execute(select(WaterQuality).filter(WaterQuality.sample_id == sample_id))
    water_quality = result.scalars().first()

    if not water_quality:
        raise HTTPException(status_code=404, detail="Sample not found")

    # Query related chemical and physical properties
    chemical_properties = (await db.execute(select(ChemicalProperties).filter(ChemicalProperties.sample_id == sample_id))).scalars().first()
    physical_properties = (await db.execute(select(PhysicalProperties).filter(PhysicalProperties.sample_id == sample_id))).scalars().first()

    response = {
        "sample_id": water_quality.sample_id,
        "potability": water_quality.potability,
        "chemical_properties": {
            "ph": chemical_properties.ph,
            "chloramines": chemical_properties.chloramines,
            "sulfate": chemical_properties.sulfate,
            "conductivity": chemical_properties.conductivity,
            "organic_carbon": chemical_properties.organic_carbon,
            "trihalomethanes": chemical_properties.trihalomethanes,
        },
        "physical_properties": {
            "hardness": physical_properties.hardness,
            "solids": physical_properties.solids,
            "turbidity": physical_properties.turbidity,
        },
    }
    return response




# Define the POST route within the router
@router.post("/sample", response_model=WaterQualityResponseSchema)
async def create_water_quality(
    sample_data: CreateSampleRequestSchema, db: AsyncSession = Depends(get_db)
):
    try:
        # Create new WaterQuality entry
        new_water_quality = WaterQuality(
            sample_id=sample_data.sample_id,
            potability=sample_data.potability
        )
        
        # Add to session and commit
        db.add(new_water_quality)
        await db.flush()  # Ensure we get the sample_id for the related tables

        # Create related ChemicalProperties entry
        new_chemical_properties = ChemicalProperties(
            sample_id=new_water_quality.sample_id,
            ph=sample_data.chemical_properties.ph,
            chloramines=sample_data.chemical_properties.chloramines,
            sulfate=sample_data.chemical_properties.sulfate,
            conductivity=sample_data.chemical_properties.conductivity,
            organic_carbon=sample_data.chemical_properties.organic_carbon,
            trihalomethanes=sample_data.chemical_properties.trihalomethanes,
        )

        # Create related PhysicalProperties entry
        new_physical_properties = PhysicalProperties(
            sample_id=new_water_quality.sample_id,
            hardness=sample_data.physical_properties.hardness,
            solids=sample_data.physical_properties.solids,
            turbidity=sample_data.physical_properties.turbidity,
        )

        # Add related properties to session and commit
        db.add(new_chemical_properties)
        db.add(new_physical_properties)

        await db.commit()

        return {
            "sample_id": new_water_quality.sample_id,
            "potability": new_water_quality.potability,
            "chemical_properties": {
                "ph": new_chemical_properties.ph,
                "chloramines": new_chemical_properties.chloramines,
                "sulfate": new_chemical_properties.sulfate,
                "conductivity": new_chemical_properties.conductivity,
                "organic_carbon": new_chemical_properties.organic_carbon,
                "trihalomethanes": new_chemical_properties.trihalomethanes,
            },
            "physical_properties": {
                "hardness": new_physical_properties.hardness,
                "solids": new_physical_properties.solids,
                "turbidity": new_physical_properties.turbidity,
            },
        }
    
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error, data may be invalid or duplicate.")
    
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

