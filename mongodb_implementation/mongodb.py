import asyncio
import pandas as pd
import motor.motor_asyncio
import os
import sys

# MongoDB connection
MONGODB_URL = "mongodb+srv://dimitrikwihangana:admin1234@waterpotability.lb4ag.mongodb.net/?retryWrites=true&w=majority&appName=waterpotability"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client['waterpotability']  # Replace with your database name

async def populate_mongodb(file_path):
    try:
        # Read the Excel file
        df = pd.read_excel(file_path, engine='openpyxl')

        for _, row in df.iterrows():
            # Insert into ChemicalProperties collection
            chemical_props = {
                "ph": row['ph'],
                "chloramines": row['Chloramines'],
                "sulfate": row['Sulfate'],
                "conductivity": row['Conductivity'],
                "organic_carbon": row['Organic_carbon'],
                "trihalomethanes": row['Trihalomethanes']
            }
            chem_result = await db.ChemicalProperties.insert_one(chemical_props)
            
            # Insert into PhysicalProperties collection
            physical_props = {
                "hardness": row['Hardness'],
                "solids": row['Solids'],
                "turbidity": row['Turbidity']
            }
            phys_result = await db.PhysicalProperties.insert_one(physical_props)

            # Insert into WaterQuality collection, referencing the inserted documents
            water_quality = {
                "potability": row['Potability'],
                "chemical_properties_id": chem_result.inserted_id,
                "physical_properties_id": phys_result.inserted_id
            }
            await db.WaterQuality.insert_one(water_quality)

        print("Data inserted successfully")

    except Exception as e:
        print(f"Error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    file_path = "new_one.xlsx"
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist")
        sys.exit(1)

    asyncio.run(populate_mongodb(file_path))
