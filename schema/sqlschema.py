from pydantic import BaseModel
from typing import Optional

# Schema for ChemicalProperties
class ChemicalPropertiesSchema(BaseModel):
    ph: float
    chloramines: float
    sulfate: float
    conductivity: float
    organic_carbon: float
    trihalomethanes: float

    class Config:
        orm_mode = True

# Schema for PhysicalProperties
class PhysicalPropertiesSchema(BaseModel):
    hardness: float
    solids: float
    turbidity: float

    class Config:
        orm_mode = True

# Schema for the incoming POST request
class CreateSampleRequestSchema(BaseModel):
    sample_id: int
    potability: bool
    chemical_properties: ChemicalPropertiesSchema
    physical_properties: PhysicalPropertiesSchema

    class Config:
        orm_mode = True

# Schema for WaterQuality response
class WaterQualityResponseSchema(BaseModel):
    sample_id: int
    potability: bool
    chemical_properties: ChemicalPropertiesSchema
    physical_properties: PhysicalPropertiesSchema

    class Config:
        orm_mode = True
