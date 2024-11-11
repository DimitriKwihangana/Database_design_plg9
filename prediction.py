import requests
import joblib
import numpy as np
import pandas as pd

# Load the trained model
model = joblib.load("model/water_quality_model.pkl")

# Step 1: Fetch the Latest MongoDB Entry
mongo_url = "http://127.0.0.1:8000/mongo/get_latest"
response = requests.get(mongo_url)

# Check if the API response is successful
if response.status_code == 200:
    latest_entry = response.json()
else:
    raise Exception("Failed to fetch data from MongoDB")

# Step 2: Prepare Data for Prediction
# Convert the API response to a DataFrame format
data = pd.DataFrame([latest_entry])

# Handle any missing values in the data (optional, adjust as necessary based on model requirements)
data = data.fillna(data.median())  # Fill missing values with median, if any

# Convert DataFrame to numpy array and ensure the correct shape for model input
input_data = np.array(data.values).reshape(1, -1)

# Step 3: Make a Prediction
prediction = model.predict(input_data)
potability = "Potable" if prediction[0] == 1 else "Non-potable"
print(f"Water potability prediction: {potability}")
