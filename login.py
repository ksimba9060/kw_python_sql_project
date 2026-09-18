from database import supabase


def login() -> str:
    """이메일과 비밀번호로 로그인하고 로그인한 사용자의 ID를 반환한다."""
    email = input("이메일: ").strip()
    password = input("비밀번호: ").strip()

    try:
        login_response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )

        user_id = login_response.user.id

        print("로그인 성공")
        print("현재 user_id:", user_id)
        return user_id

    except Exception as error:
        print("로그인 실패:", error)
        raise SystemExit from error
