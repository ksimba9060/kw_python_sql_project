from reservation.game_service import select_game
from reservation.reservation_service import show_reservation
from reservation.seat_service import select_seat


def run_reservation() -> None:
    """경기 예매 메뉴를 실행한다."""
    print("\n=== 경기 예매 ===")
    print("1. 경기 예매")
    print("2. 예매 내역 조회")
    print("0. 이전 메뉴")

    choice = input("메뉴를 선택하세요: ").strip()

    if choice == "1":
        game_id = select_game()
        if game_id is not None:
            selected_seat = select_seat(game_id)
    elif choice == "2":
        show_reservation()
    elif choice != "0":
        print("올바른 메뉴 번호를 입력하세요.")
