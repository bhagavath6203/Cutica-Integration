import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    MONGO_USERNAME = os.getenv('MONGO_USERNAME')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
    
    if MONGO_USERNAME is None or MONGO_PASSWORD is None:
        raise ValueError("Environment variables MONGO_USERNAME and MONGO_PASSWORD must be set")
    
    MONGO_URI = f"mongodb+srv://bhagavath11ab:01012002@cluster0.tsgk9f6.mongodb.net/cutica_db?retryWrites=true&w=majority&appName=Cluster0"

    ATLAS_API_KEY_PUBLIC = os.getenv('ATLAS_API_KEY_PUBLIC')
    ATLAS_API_KEY_PRIVATE = os.getenv('ATLAS_API_KEY_PRIVATE')
    ATLAS_GROUP_ID = os.getenv('ATLAS_GROUP_ID')
    
    GOOGLE_CREDENTIALS_PATH = 'auth/credentials.json'
    GOOGLE_TOKEN_PATH = 'auth/token.pickle'
