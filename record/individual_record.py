def show_individual_record(role: str) -> None:
    """선택한 투수 또는 타자의 개인 기록을 조회한다."""
    role_name = "투수" if role == "pitcher" else "타자"
    print(f"{role_name} 개인 기록 조회 기능을 준비 중입니다.")
