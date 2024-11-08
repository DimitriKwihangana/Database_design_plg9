import asyncio
import uvicorn
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from mongodbmodel import WaterQuality
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

import joblib

model = joblib.load("model.pkl")

# creating an app instance 
app = FastAPI() 

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Allow GET and POST requests
    allow_headers=["*"],  # Allow any headers
)

# create a pedantic class for the request
class WaterPRequest(BaseModel):
    ph: float = Field(gt=0, lt=1000.0)
    Hardness: float = Field(gt=0, lt=1000.000)
    Solids: float = Field(gt=0, lt=1000.0)
    Chloramines: float = Field(gt=0, lt=1000.000)
    Sulfate: float = Field(gt=0, lt=1000.0)
    Conductivity: float = Field(gt=0, lt=1000.000)
    Organic_carbon: float = Field(gt=0, lt=1000.0)
    Trihalomethanes: float = Field(gt=0, lt=1000.0)
    Turbidity: float = Field(gt=0, lt=1000.0)
 
# class testing 
@app.get("/class")
async def get_greet():
    return {"Message": "Hello API"}


@app.get("/", status_code=status.HTTP_200_OK)
async def get_hello():
    return {"hello": "PLG9"}

@app.post('/predict', status_code=status.HTTP_200_OK)
async def make_prediction(waterp_request: WaterPRequest):
    try:
        single_row = [[waterp_request.ph, waterp_request.Hardness, waterp_request.Solids, waterp_request.Chloramines, waterp_request.Sulfate , waterp_request.Conductivity , waterp_request.Organic_carbon, waterp_request.Trihalomethanes, waterp_request.Turbidity]]
        new_value = model.predict(single_row)
        integer_quality = int(new_value[0])  # Convert the predicted value to an integer
        return {"predicted Quality": integer_quality}
        
    #except:
    #    raise HTTPException(status_code=500, detail="Something went wrong.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))