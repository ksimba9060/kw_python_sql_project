from database import supabase


def select_game() -> None:
    """경기 일정을 조회하고 예매할 경기를 선택한다."""
    print("경기 일정 조회 및 선택 기능을 준비 중입니다.")

    response = (
        supabase
        .schema("team_4")
        .table("game_info")
        .select("*")
        .order("game_date")
        .execute()
    )

    games = response.data

    if not games:
        print("등록된 경기가 없습니다.")
        return None

    print("\n===== SSG 경기 일정 =====")

    for game in games:
        print(
            f"{game['game_id']}. "
            f"SSG vs {game['opponent_team']} | "
            f"{game['game_date']} {game['game_time']} | "
            f"{game['stadium']}"
        )

    while True:
        try:
            game_id = int(input("\n예매할 경기 번호를 선택하세요: "))

            selected_game = None

            for game in games:
                if game["game_id"] == game_id:
                    selected_game = game
                    break

            if selected_game is None:
                print("존재하지 않는 경기입니다.")
                continue

            print("\n선택한 경기")
            print(
                f"SSG vs {selected_game['opponent_team']} | "
                f"{selected_game['game_date']} "
                f"{selected_game['game_time']}"
            )

            return game_id

        except ValueError:
            print("숫자로 입력해주세요.")


select_game()