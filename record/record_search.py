from record.individual_record import show_individual_record
from record.team_record import show_team_record


def run_record_search() -> None:
    """투수/타자 및 개인/팀 기록 검색 메뉴를 실행한다."""
    print("\n=== 선수 기록 검색 ===")
    print("1. 개인 기록")
    print("2. 팀 전체 기록")
    print("0. 이전 메뉴")

    choice = input("조회 범위를 선택하세요: ").strip()

    if choice not in {"1", "2"}:
        if choice != "0":
            print("올바른 메뉴 번호를 입력하세요.")
        return

    print("\n1. 투수 기록")
    print("2. 타자 기록")
    role_choice = input("선수 유형을 선택하세요: ").strip()

    role_by_choice = {"1": "pitcher", "2": "batter"}
    role = role_by_choice.get(role_choice)
    if role is None:
        print("올바른 메뉴 번호를 입력하세요.")
        return

    if choice == "1":
        show_individual_record(role)
    else:
        show_team_record(role)
