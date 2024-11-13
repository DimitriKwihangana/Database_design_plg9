import asyncio
import pandas as pd
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import ChemicalProperties, PhysicalProperties, WaterQuality
import sys
import os

# Define database URL and models
DATABASE_URL = "postgresql+asyncpg://root:vs1kol6cpH9KmVe0U8hVuO52sdwv2MeF@dpg-csl7uqe8ii6s73c181ag-a.oregon-postgres.render.com/customer_database_5rln"

# Create engine and session
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def populate_db(file_path):
    async with SessionLocal() as session:
        try:
            # Read Excel file
            df = pd.read_excel(file_path, engine='openpyxl')

            for _, row in df.iterrows():
                chemical_props = ChemicalProperties(
                    ph=row['ph'],
                    chloramines=row['Chloramines'],
                    sulfate=row['Sulfate'],
                    conductivity=row['Conductivity'],
                    organic_carbon=row['Organic_carbon'],
                    trihalomethanes=row['Trihalomethanes']
                )
                session.add(chemical_props)
                await session.flush()  # Get the ID of the newly inserted row

                physical_props = PhysicalProperties(
                    hardness=row['Hardness'],
                    solids=row['Solids'],
                    turbidity=row['Turbidity']
                )
                session.add(physical_props)
                await session.flush()  # Get the ID of the newly inserted row

                water_quality = WaterQuality(
                    potability=row['Potability'],
                    chemical_properties_id=chemical_props.id,
                    physical_properties_id=physical_props.id
                )
                session.add(water_quality)

            # Commit the session
            await session.commit()

        except Exception as e:
            await session.rollback()
            print(f"Error occurred: {e}", file=sys.stderr)
        finally:
            await session.close()

if __name__ == "__main__":
    file_path = "new_one.xlsx"
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist")
        sys.exit(1)

    asyncio.run(populate_db(file_path))
