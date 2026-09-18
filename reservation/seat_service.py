import sys
from pathlib import Path


if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from database import supabase

def select_seat(game_id):

    try:
        response = (
            supabase
            .schema("team_4")
            .table("game_seats")
            .select("*")
            .eq("game_id", game_id)
            .execute()
        )
    except Exception as error:
        print(f"좌석 정보를 불러오지 못했습니다: {error}")
        return None

    seats = response.data or []

    print("DEBUG response:", response.data)
    print("DEBUG game_id:", game_id)

    if not seats:
        print(f"선택한 경기(game_id={game_id})에 등록된 좌석 정보가 없습니다.")
        return None

    print("\n===== 좌석 정보 =====")

    seat_groups = {}
    for seat in seats:
        seat_groups.setdefault(seat["seat_grade"], []).append(seat)

    for seat_grade, grade_seats in seat_groups.items():
        print(f"\n[{seat_grade}]")
        for seat in grade_seats:
            print(
                f"{seat['game_seat_id']}. "
                f"{seat['price']:,}원 | "
                f"잔여 좌석 {seat['remaining_seats']}석"
            )

    while True:
        try:
            game_seat_id = int(input("\n좌석 번호를 선택하세요: "))

            selected_seat = None

            for seat in seats:
                if seat["game_seat_id"] == game_seat_id:
                    selected_seat = seat
                    break

            if selected_seat is None:
                print("존재하지 않는 좌석입니다.")
                continue

            if selected_seat["remaining_seats"] <= 0:
                print("매진된 좌석입니다.")
                continue

            quantity = int(input("예매 수량을 입력하세요: "))

            if quantity <= 0:
                print("예매 수량은 1장 이상이어야 합니다.")
                continue

            if quantity > selected_seat["remaining_seats"]:
                print(
                    f"잔여 좌석이 부족합니다. "
                    f"현재 {selected_seat['remaining_seats']}석 남아 있습니다."
                )
                continue

            total_price = selected_seat["price"] * quantity

            print("\n===== 선택 정보 =====")
            print(f"좌석 등급: {selected_seat['seat_grade']}")
            print(f"예매 수량: {quantity}장")
            print(f"총 금액: {total_price:,}원")

            return {
                "game_seat_id": game_seat_id,
                "seat_grade": selected_seat["seat_grade"],
                "price": selected_seat["price"],
                "quantity": quantity,
                "total_price": total_price,
                "remaining_seats": selected_seat["remaining_seats"]
            }

        except ValueError:
            print("숫자로 입력해주세요.")
