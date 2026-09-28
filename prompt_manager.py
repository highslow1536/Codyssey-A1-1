"""메모리에만 저장되는 콘솔 프롬프트 관리 프로그램."""

from sample_prompts import load_sample_prompts


def show_menu():
    print("\n=== 나만의 프롬프트 관리 ===")
    print("0. 종료")


def main():
    prompts = load_sample_prompts()
    while True:
        show_menu()
        choice = input("선택: ").strip()
        if choice == "0":
            print("프로그램을 종료합니다.")
            break
        print("올바른 메뉴 번호를 입력해주세요.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\n프로그램을 종료합니다.")
