import pandas as pd
from supabase import create_client
SUPABASE_URL = "https://gcbrqpjbbzlbelksidqw.supabase.co"
SUPABASE_KEY = "sb_publishable_y-YrLOSq5O2LP6r2o9BTBw_NAlfrlJ8"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
#### 로컬에서 돌려보려고 필요한 부분 


def show_team_record(role: str) -> None:
    """선택한 투수 또는 타자의 팀 전체 기록을 조회한다."""
    role_name = "투수" if role == "pitcher" else "타자"
    if role == "pitcher":
        pitcher_team_record()
    elif role == 'batter':
        hitter_team_record()

def pitcher_team_record():
    team_era = calculate_team_era(0,1) ## 제약조건이 없는 경우 첫번째 변수를 0으로 넣음
    print(f"팀의 평균 era는 {team_era:.2f}입니다.")

    right_era = calculate_team_era("throw_hand","우투")
    print(f"팀의 평균 우투 era는 {right_era:.2f}입니다.")
    left_era = calculate_team_era("throw_hand","좌투")
    print(f"팀의 평균 우투 era는 {left_era:.2f}입니다.")

    선발_era = calculate_team_era("pitcher_role","선발")
    print(f"팀의 평균 era는 {선발_era:.2f}입니다.")
    중간_era = calculate_team_era("pitcher_role","중간")
    print(f"팀의 평균 era는 {중간_era:.2f}입니다.")
    마무리_era = calculate_team_era("pitcher_role","마무리")
    print(f"팀의 평균 era는 {마무리_era:.2f}입니다.")

def hitter_team_record():
    team_avg = calculate_team_avg_hit(0,1) ## 제약조건이 없는 경우 첫번째 변수를 0으로 넣음
    print(f"팀의 평균 타율은 {team_avg:.2f}입니다.")

    right_avg = calculate_team_era("target_left_right","우타")
    print(f"팀의 평균 우타 타율은 {right_avg:.2f}입니다.")
    left_avg = calculate_team_era("target_left_right","좌타")
    print(f"팀의 평균 좌타 타율은 {left_avg:.2f}입니다.")

    in_avg = calculate_team_era("target_position","내야수")
    print(f"팀의 평균 내야수 타율은 {in_avg:.2f}입니다.")
    out_avg = calculate_team_era("target_position","외야수")
    print(f"팀의 평균 외야수 타율은 {out_avg:.2f}입니다.")    
    catch_avg = calculate_team_era("target_position","포수")
    print(f"팀의 평균 포수 타율은 {catch_avg:.2f}입니다.")

def parse_baseball_innings(ip_value: float) -> float:
    # 야구 이닝 표기법(.1 -> 1/3, .2 -> 2/3)을 실제 수치로 변환합니다.
    full_innings = int(ip_value)
    outs = round((ip_value - full_innings) * 10)  # .1 이면 1아웃, .2 이면 2아웃
    return full_innings + (outs / 3.0)

def calculate_team_era(제약변수, 조건):
    # Supabase에서 투수 데이터 조회
    if 제약변수 == 0: #제야변수가 없는 경우 전부 불러오기.
        response = (
                supabase.schema("team_4")
                .table("pitchers")
                .select("era, innings")
                .execute()
        )
    else:
        response = (
            supabase.schema("team_4")
            .table("pitchers")
            .select("era, innings")
            .eq(제약변수, 조건)
            .execute()
        )
    
    pitchers = response.data
    if not pitchers:
        print("조회된 투수 데이터가 없습니다.")
        return

    total_earned_runs = 0.0  # 총 자책점 합계
    total_innings = 0.0      # 총 이닝수 합계

    for p in pitchers:
        era = float(p.get("era") or 0.0)
        raw_innings = float(p.get("innings") or 0.0)

        # 야구 이닝 표기 변환 (.1, .2 처리)
        real_innings = parse_baseball_innings(raw_innings)

        # 9이닝 당 개인 자책점 = era * 이닝수
        earned_runs = era * real_innings

        total_earned_runs += earned_runs
        total_innings += real_innings

    # 팀 평균 ERA 계산
    if total_innings > 0:
        team_era = total_earned_runs / total_innings
        return team_era
    else:
        print("유효한 이닝 데이터가 없습니다.")
        return None


def calculate_team_avg_hit(제약변수, 조건):
    if 제약변수 == 0 :
            res1 = supabase.schema("team_4").rpc("get_team_avg").execute()
    else :
        res1 = supabase.schema("team_4").rpc("get_team_avg", {
            제약변수 : 조건 
        }).execute()
    return res1


show_team_record("pitcher")