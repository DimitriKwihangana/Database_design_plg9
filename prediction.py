import requests
import joblib
import numpy as np
import pandas as pd
import sys
import io

# Load the trained model
model = joblib.load("model/water_quality_model.pkl")

mongo_url = "http://127.0.0.1:8000/water_quality"  # Your FastAPI endpoint
response = requests.get(mongo_url)


if response.status_code == 200:
    all_entries = response.json()  # Assuming it returns a list of entries
else:
    raise Exception("Failed to fetch data from SQL")

# Step 2: Get the Last Entry (Most Recent)
if len(all_entries) == 0:
    raise Exception("No data available to predict")


latest_entry = all_entries[-1]

print(latest_entry,'latest entry_______')
# Step 3: Prepare Data for Prediction
# Convert the last entry to a DataFrame format
data = pd.DataFrame([latest_entry])

# Inspect the columns of the data
print(data.columns)  # This will help you identify any extra columns

data = data[['ph', 'chloramines', 'sulfate', 'conductivity', 'organic_carbon',
             'trihalomethanes', 'hardness', 'solids', 'turbidity']]  # Adjust the column names

print(data,'data___________')
# Convert DataFrame to numpy array and ensure the correct shape for model input
input_data = np.array(data.values).reshape(1, -1)

# Step 4: Make a Prediction
prediction = model.predict(input_data)

# Convert prediction to potability status
potability = "Potable" if prediction[0] == 1 else "Non-potable"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Now try printing
print(f"Water potability prediction: {potability}")
