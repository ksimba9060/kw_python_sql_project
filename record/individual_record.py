from database import supabase


def show_individual_record(role: str) -> None:
    """선택한 투수 또는 타자의 개인 기록을 조회한다."""

    role_name = "투수" if role == "pitcher" else "타자"

    print(f"\n=== {role_name} 개인 기록 ===")

    # 선수 이름 입력
    player_name = input("선수 이름을 입력하세요: ").strip()

    # players 테이블에서 입력한 선수 검색
    response = (
        supabase
        .schema("team_4")
        .table("players")
        .select("*")
        .eq("player_name", player_name)
        .execute()
    )

    # 입력한 이름의 선수가 없는 경우
    if not response.data:
        print("해당 이름의 선수가 존재하지 않습니다.")
        return

    # 검색한 선수의 player_id 가져오기
    player_id = response.data[0]["player_id"]


    # =========================
    # 투수 개인 기록
    # =========================
    if role == "pitcher":

        record = (
            supabase
            .schema("team_4")
            .table("pitchers")
            .select("*")
            .eq("player_id", player_id)
            .execute()
        )

        # 선수는 존재하지만 투수 기록이 없는 경우
        if not record.data:
            print("해당 선수의 투수 기록이 존재하지 않습니다.")
            return

        pitcher = record.data[0]

        print(f"\n=== {player_name} 선수 기록 ===")
        print(f"누적 이닝 : {pitcher['innings']}")
        print(f"ERA : {pitcher['era']}")
        print(f"세이브 : {pitcher['saves']}")
        print(f"홀드 : {pitcher['holds']}")
        print(f"WHIP : {pitcher['whip']}")
        print(f"투구 : {pitcher['throw_hand']}")
        print(f"역할 : {pitcher['pitcher_role']}")


    # =========================
    # 타자 개인 기록
    # =========================
    elif role == "batter":

        record = (
            supabase
            .schema("team_4")
            .table("hitters")
            .select("*")
            .eq("player_id", player_id)
            .execute()
        )

        # 선수는 존재하지만 타자 기록이 없는 경우
        if not record.data:
            print("해당 선수의 타자 기록이 존재하지 않습니다.")
            return

        hitter = record.data[0]

        print(f"\n=== {player_name} 선수 기록 ===")
        print(f"타율 : {hitter['avg']}")
        print(f"타수 : {hitter['at_bats']}")
        print(f"안타 : {hitter['hit']}")
        print(f"득점 : {hitter['run']}")
        print(f"홈런 : {hitter['home_run']}")
        print(f"좌/우타 : {hitter['left_right']}")
        print(f"포지션 : {hitter['hitter_position']}")