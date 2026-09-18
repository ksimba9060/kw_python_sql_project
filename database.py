import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import Client, create_client


load_dotenv(Path(__file__).resolve().parent / ".env.example")

url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]

supabase: Client = create_client(url, key)


if __name__ == "__main__":
    print("Supabase Client 생성 완료")
