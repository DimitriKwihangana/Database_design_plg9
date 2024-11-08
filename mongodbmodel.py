from pydantic import BaseModel, Field
from typing import List, Optional


class WaterQuality(BaseModel):
    
    potability: bool
    ph: Optional[float] = None
    chloramines: Optional[float] = None
    sulfate: Optional[float] = None
    conductivity: Optional[float] = None
    organic_carbon: Optional[float] = None
    trihalomethanes: Optional[float] = None
    hardness: Optional[float] = None
    solids: Optional[float] = None
    turbidity: Optional[float] = None
