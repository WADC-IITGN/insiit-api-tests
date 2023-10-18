import os
from dotenv import load_dotenv

load_dotenv()

url = f"http://localhost:{int(os.getenv('PORT'))}"
api_key = os.getenv("API_KEY")
