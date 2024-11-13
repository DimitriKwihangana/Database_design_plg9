from pydantic import BaseModel

class WaterQuality(BaseModel):
    potability: int
    ph: float
    chloramines: float
    sulfate: float
    conductivity: float
    organic_carbon: float
    trihalomethanes: float
    hardness: float
    solids: float
    turbidity: float

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "potability": 1,
                "ph": 7.2,
                "chloramines": 4.0,
                "sulfate": 300.0,
                "conductivity": 450.0,
                "organic_carbon": 2.5,
                "trihalomethanes": 80.0,
                "hardness": 120.0,
                "solids": 21000.0,
                "turbidity": 3.0
            }
        }


