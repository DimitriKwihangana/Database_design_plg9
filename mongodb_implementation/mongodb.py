import pandas as pd
from pymongo import MongoClient

# Connecting to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["water_potability_db"]

import os
print(os.getcwd()) 


# Load the dataset
file_path = 'water_potability.csv'
dataset = pd.read_csv(file_path)
dataset['SampleID'] = range(1, len(dataset) + 1)
print(dataset)



# Collections and Data insertetion
Samples_Collection = {
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["locationId", "sampleDate", "potability"],
    "properties": {
       "locationId": {"bsonType": "objectId", "description": "Reference to the location of the water sample."},
       "sampleDate": {"bsonType": "date", "description": "Date when the sample was collected."},
       "potability": {"bsonType": "int", "enum": [0, 1], "description": "Indicates if the water is potable (1) or not potable (0)."}
    }
  }
}

ChemicalProperties_Collection = {
  "$jsonSchema": {
     "bsonType": "object",
     "required": ["sampleId", "ph", "hardness", "solids", "chloramines", "sulfate"],
     "properties": {
       "sampleId": {"bsonType": "objectId",  "description": "Reference to the sample in the Samples collection."},

       "ph": {"bsonType": "double", "description": "pH level of the water sample."},

       "hardness": {"bsonType": "double", "description": "Hardness level of the water sample."},

       "solids": {"bsonType": "double", "description": "Solids concentration in the water sample."},

       "chloramines": {"bsonType": "double", "description": "Chloramines concentration in the water sample."},

       "sulfate": {"bsonType": "double", "description": "Sulfate concentration in the water sample."}
     }
  }
}

PhysicalProperties_Collection = {
   "$jsonSchema": {
     "bsonType": "object",
     "required": ["sampleId", "conductivity", "organicCarbon", "trihalomethanes", "turbidity"],
     "properties": {
       "sampleId":{"bsonType": "objectId", "description": "Reference to the sample in the Samples collection."},

        "conductivity": {"bsonType": "double", "description": "Conductivity of the water sample."},

        "organicCarbon": {"bsonType": "double", "description": "Organic carbon concentration in the water sample."},

        "trihalomethanes": {"bsonType": "double", "description": "Trihalomethanes concentration in the water sample."},

        "turbidity": {"bsonType": "double", "description": "Turbidity level of the water sample."}
     }
   }
}

def create_or_update_collection(collection_name, schema):
    if collection_name in db.list_collection_names():
        db.command({"collMod": collection_name, "validator": schema})
    else:
        db.create_collection(collection_name, validator=schema)

create_or_update_collection("Samples", Samples_Collection)
create_or_update_collection("ChemicalProperties", ChemicalProperties_Collection)
create_or_update_collection("PhysicalProperties", PhysicalProperties_Collection)

print("Collections updated with schema validation successfully!")