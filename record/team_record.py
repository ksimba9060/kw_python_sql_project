def show_team_record(role: str) -> None:
    """선택한 투수 또는 타자의 팀 전체 기록을 조회한다."""
    role_name = "투수" if role == "pitcher" else "타자"
    print(f"{role_name} 팀 전체 기록 조회 기능을 준비 중입니다.")
    if role == "pitcher":
        pitcher_team_record()
        """ 
    elif role == 'batter':
        batter_team_record() """
    


import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]

supabase: Client = create_client(url, key)
print("Supabase Client 생성 완료")
""" 
def pitcher_team_record():

 """