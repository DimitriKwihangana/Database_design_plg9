from pymongo.mongo_client import MongoClient

MONGODB_URL = "mongodb+srv://dimitrikwihangana:admin1234@waterpotability.lb4ag.mongodb.net/?retryWrites=true&w=majority&appName=waterpotability"
client = MongoClient(MONGODB_URL)

db = client.water_potability

collection_name = db["water_potability"]