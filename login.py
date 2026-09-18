from database import supabase


def login() -> dict:
    """로그인한 사용자와 연결된 고객 정보를 조회해 반환한다."""
    email = input("이메일: ").strip()
    password = input("비밀번호: ").strip()

    try:
        login_response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )
    except Exception as error:
        print("로그인 실패:", error)
        raise SystemExit from error

    if login_response.user is None:
        print("로그인 실패: 사용자 정보를 확인할 수 없습니다.")
        raise SystemExit

    user_id = login_response.user.id

    try:
        customer_response = (
            supabase.schema("team_4")
            .table("customers")
            .select("*")
            .eq("auth_user_id", user_id)
            .limit(1)
            .execute()
        )
    except Exception as error:
        print("고객 정보 조회 실패:", error)
        raise SystemExit from error

    if not customer_response.data:
        print("로그인은 성공했지만 연결된 고객 정보가 없습니다.")
        raise SystemExit

    customer = customer_response.data[0]

    print("로그인 성공")
    print("고객 번호:", customer["customer_id"])
    print("고객 이름:", customer["customer_name"])
    print("이메일:", customer["email"])

    return customer
