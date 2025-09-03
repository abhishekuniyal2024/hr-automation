from dotenv import load_dotenv, find_dotenv
import os

dotenv_path = find_dotenv()
print("Found .env at:", dotenv_path)  # check if it’s found

load_dotenv(dotenv_path)
api_key = os.getenv("GROQ_API_KEY")

print("API Key:", api_key if api_key else "NOT FOUND")

