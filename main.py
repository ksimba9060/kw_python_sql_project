from login import login
from record.record_search import run_record_search
from reservation.reservation_main import run_reservation


def main() -> None:
    login()

    while True:
        print("\n=== 야구팀 정보 검색 / 예매 ===")
        print("1. 선수 기록 검색")
        print("2. 경기 예매")
        print("0. 종료")

        choice = input("메뉴를 선택하세요: ").strip()

        if choice == "1":
            run_record_search()
        elif choice == "2":
            run_reservation()
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("올바른 메뉴 번호를 입력하세요.")


if __name__ == "__main__":
    main()
