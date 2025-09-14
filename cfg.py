from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    TOKEN = os.getenv("TOKEN_")
    BASE_URL=os.getenv('BASE_URL_')
    API_KEY_AI=os.getenv('API_KEY_AI_')
    MODEL=os.getenv('MODEL_')