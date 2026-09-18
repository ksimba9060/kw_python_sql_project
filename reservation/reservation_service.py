
from reservation.seat_service import select_seat

def create_reservation(supabase, customer_id: int) -> None:
    """예매번호를 생성하고 예매 내역을 저장한다."""
    try:
        # 1. 예매 수량 및 좌석 입력
        game_seat_id = select_seat(game_seat_id)
        if not game_seat_id:
            return
        
        quantity = int(input("예매 수량을 입력하세요: "))     
        if quantity <= 0:
            print("수량은 1 이상이어야 합니다.")
            return
            
        print("예매를 진행 중입니다...")

        # 2. 잔여 좌석 및 가격 조회
        seat_result = (
            supabase
            .schema("team_4")
            .table("game_seats")
            .select("remaining_seats, price")
            .eq("game_seat_id", game_seat_id)
            .execute()
        )

        if len(seat_result.data) == 0:
            print("존재하지 않는 좌석입니다.")
            return

        seat_data = seat_result.data[0]
        current_seats = int(seat_data["remaining_seats"])
        price = int(seat_data["price"])

        # 3. 잔여 좌석 < 구매 수량 -> 부족
        if current_seats < quantity:
            print(f"잔여 좌석이 부족합니다. (현재 잔여: {current_seats}석)")
            return

        # 4. 좌석 차감
        new_seats = current_seats - quantity
        (
            supabase
            .schema("team_4")
            .table("game_seats")
            .update({"remaining_seats": new_seats})
            .eq("game_seat_id", game_seat_id)
            .execute()
        )

        # 5. 예매 내역 등록 및 예매번호 생성
        total_price = price * quantity
        insert_result = (
            supabase
            .schema("team_4")
            .table("reservations")
            .insert({
                "customer_id": customer_id,
                "game_seat_id": game_seat_id,
                "quantity": quantity,
                "total_price": total_price
            })
            .execute()
        )

        # 6. 예매 성공 출력
        reservation_id = insert_result.data[0]["reservation_id"]
        print("\n[예매 완료] 예매가 성공적으로 처리되었습니다!")
        print(f"부여된 예매 번호는 [{reservation_id}] 입니다. 내역 조회 시 사용해주세요.")
        
    except ValueError:
        print("\n[입력 오류] 올바른 숫자를 입력해주세요.")
    except Exception as e:
        print(f"\n[예매 실패] 시스템 오류가 발생했습니다: {e}")


def show_reservation(supabase) -> None:
    """예매번호로 예매 내역을 조회한다."""
    try:
        # 1. 예매 번호 입력
        res_id = int(input("조회할 예매 번호를 입력하세요: "))
    except ValueError:
        print("숫자만 입력 가능합니다.")
        return

    try:
        # 2. 예매 내역 기본 정보 조회
        res_result = (
            supabase
            .schema("team_4")
            .table("reservations")
            .select("customer_id, game_seat_id, quantity, total_price, reservation_date")
            .eq("reservation_id", res_id)
            .execute()
        )

        if len(res_result.data) == 0:
            print("\n해당 번호의 예매 내역이 존재하지 않습니다.")
            return
        
        res_data = res_result.data[0]

        # 3. 선택 좌석 정보 조회
        seat_result = (
            supabase
            .schema("team_4")
            .table("game_seats")
            .select("game_id, seat_grade")
            .eq("game_seat_id", res_data["game_seat_id"])
            .execute()
        )
        seat_data = seat_result.data[0]

        # 4. 경기 정보 (상대팀) 조회
        game_result = (
            supabase
            .schema("team_4")
            .table("games")
            .select("opponent_team")
            .eq("game_id", seat_data["game_id"])
            .execute()
        )
        game_data = game_result.data[0]

        # 5. 예매자 정보 조회
        cust_result = (
            supabase
            .schema("team_4")
            .table("customers")
            .select("customer_name")
            .eq("customer_id", res_data["customer_id"])
            .execute()
        )
        cust_data = cust_result.data[0]

        # 6. 내역 상세 출력
        print("\n===============================")
        print(f" 예매 번호 : {res_id}")
        print(f" 예매 날짜 : {res_data['reservation_date']}")
        print(f" 예매자명  : {cust_data['customer_name']}")
        print(f" 경기 정보 : SSG vs {game_data['opponent_team']}")
        print(f" 선택 좌석 : {seat_data['seat_grade']}")
        print(f" 구매 수량 : {res_data['quantity']}매")
        print(f" 총 금액   : {res_data['total_price']:,}원")
        print("===============================")
        
    except Exception as e:
        print(f"\n[조회 실패] 시스템 오류가 발생했습니다: {e}")