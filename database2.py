from mongoengine import Document, FloatField, IntField, ReferenceField, connect

# Connect to MongoDB (replace with your database URI and name)
connect('plg_9', host='mongodb://localhost:27017/your_database_name')


# Define the ChemicalProperties collection
class ChemicalProperties(Document):
    pH = FloatField()
    Hardness = FloatField()
    Solids = FloatField()
    Chloramines = FloatField()
    Sulfate = FloatField()
    Organic_carbon = FloatField()
    Trihalomethanes = FloatField()

    meta = {
        'collection': 'chemical_properties',  # Collection name
    }


# Define the PhysicalProperties collection
class PhysicalProperties(Document):
    Conductivity = FloatField()
    Turbidity = FloatField()

    meta = {
        'collection': 'physical_properties',  # Collection name
    }


# Define the Samples collection, referencing the chemical and physical properties
class Samples(Document):
    potability = IntField(required=True)  # 1 for potable, 0 for not potable
    chemical_properties = ReferenceField(ChemicalProperties)  # Reference to ChemicalProperties document
    physical_properties = ReferenceField(PhysicalProperties)  # Reference to PhysicalProperties document

    meta = {
        'collection': 'samples',  # Specifies the collection name
        'ordering': ['-id']       # Orders by `_id` in descending order by default
    }


# Example function to add a sample to the database
def add_sample(potability, pH, Hardness, Solids, Chloramines, Sulfate,
               Organic_carbon, Trihalomethanes, Conductivity, Turbidity):
    
    # Create chemical properties document
    chem_props = ChemicalProperties(
        pH=pH,
        Hardness=Hardness,
        Solids=Solids,
        Chloramines=Chloramines,
        Sulfate=Sulfate,
        Organic_carbon=Organic_carbon,
        Trihalomethanes=Trihalomethanes
    )
    chem_props.save()  # Save to MongoDB

    # Create physical properties document
    phys_props = PhysicalProperties(
        Conductivity=Conductivity,
        Turbidity=Turbidity
    )
    phys_props.save()  # Save to MongoDB

    # Create a sample and reference the chemical and physical properties
    sample = Samples(
        potability=potability,
        chemical_properties=chem_props,
        physical_properties=phys_props
    )
    sample.save()  # Save to MongoDB
    print("Sample added with ID:", sample.id)


# Function to fetch and display the latest sample
def fetch_latest_sample():
    latest_sample = Samples.objects.first()  # Fetches the latest due to ordering

    if latest_sample:
        print("Latest Sample ID:", latest_sample.id)
        print("Potability:", "Potable" if latest_sample.potability == 1 else "Not Potable")
        
        # Access and print chemical properties
        chem_props = latest_sample.chemical_properties
        if chem_props:
            print("Chemical Properties:")
            print("  pH:", chem_props.pH)
            print("  Hardness:", chem_props.Hardness)
            print("  Solids:", chem_props.Solids)
            print("  Chloramines:", chem_props.Chloramines)
            print("  Sulfate:", chem_props.Sulfate)
            print("  Organic Carbon:", chem_props.Organic_carbon)
            print("  Trihalomethanes:", chem_props.Trihalomethanes)
        
        # Access and print physical properties
        phys_props = latest_sample.physical_properties
        if phys_props:
            print("Physical Properties:")
            print("  Conductivity:", phys_props.Conductivity)
            print("  Turbidity:", phys_props.Turbidity)
    else:
        print("No samples found in the database.")


# Example usage
if __name__ == "__main__":
    # Add a new sample
    add_sample(
        potability=1,  # 1 for potable, 0 for not potable
        pH=7.1,
        Hardness=120.5,
        Solids=215.0,
        Chloramines=8.0,
        Sulfate=250.0,
        Organic_carbon=20.5,
        Trihalomethanes=80.5,
        Conductivity=450.0,
        Turbidity=2.5
    )

    # Fetch and display the latest sample
    fetch_latest_sample()