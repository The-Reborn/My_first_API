# app/config.py

# Import the necessary libraries
import os  # For accessing environment variables
from dotenv import load_dotenv  # For loading environment variables from a .env file

# Load environment variables from a .env file into the process environment
load_dotenv()

# Define the base URL for the API endpoint
BASE_URL = "https://yfapi.net/v6/finance/quote"

# Define default values for region and language
REGION = "US"
LANG = "en"

# Retrieve the API key from the environment variables
# This assumes you have a .env file with an API_KEY variable
API_KEY = os.getenv("API_KEY")
