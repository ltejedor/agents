from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()  # Load from a .env file in the working directory

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
