"""메모리에만 저장되는 콘솔 프롬프트 관리 프로그램."""

from sample_prompts import load_sample_prompts

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]


def read_nonempty(label):
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print("빈 값은 입력할 수 없습니다. 다시 입력해주세요.")


def choose_category(prompts, allow_custom=False):
    categories = list(dict.fromkeys(CATEGORIES + [p["category"] for p in prompts]))
    print("카테고리 선택:")
    for number, category in enumerate(categories, 1):
        print(f"{number}. {category}")
    if allow_custom:
        print("직접 입력하려면 카테고리 이름을 입력하세요.")
    while True:
        answer = read_nonempty("선택")
        if answer.isdecimal() and 1 <= int(answer) <= len(categories):
            return categories[int(answer) - 1]
        if allow_custom and not answer.isdecimal():
            return answer
        print("올바른 카테고리 번호를 입력해주세요.")


def add_prompt(prompts):
    print("\n=== 프롬프트 추가 ===")
    title = read_nonempty("제목")
    content = read_nonempty("내용")
    category = choose_category(prompts, allow_custom=True)
    prompts.append({"title": title, "content": content, "category": category, "favorite": False})
    print("프롬프트가 추가되었습니다!")


def show_list(prompts):
    print("\n=== 프롬프트 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return
    for number, prompt in enumerate(prompts, 1):
        star = " ⭐" if prompt["favorite"] else ""
        print(f'{number}. [{prompt["category"]}] {prompt["title"]}{star}')
    print(f"총 {len(prompts)}개의 프롬프트")


def show_category(prompts):
    print("\n=== 카테고리별 조회 ===")
    category = choose_category(prompts)
    print(f"[{category}] 카테고리 프롬프트:")
    found = 0
    for number, prompt in enumerate(prompts, 1):
        if prompt["category"] == category:
            star = " ⭐" if prompt["favorite"] else ""
            print(f'{number}. {prompt["title"]}{star}')
            found += 1
    if found:
        print(f"총 {found}개의 프롬프트")
    else:
        print("해당 카테고리에 프롬프트가 없습니다.")


def search_prompt(prompts):
    print("\n=== 프롬프트 검색 ===")
    keyword = read_nonempty("검색어").casefold()
    found = 0
    for number, prompt in enumerate(prompts, 1):
        if keyword in prompt["title"].casefold() or keyword in prompt["content"].casefold():
            star = " ⭐" if prompt["favorite"] else ""
            print(f'{number}. [{prompt["category"]}] {prompt["title"]}{star}')
            found += 1
    if found:
        print(f"{found}개의 프롬프트를 찾았습니다.")
    else:
        print("검색 결과가 없습니다.")


def choose_prompt(prompts):
    answer = input("프롬프트 번호: ").strip()
    if not answer.isdecimal() or not 1 <= int(answer) <= len(prompts):
        print("올바른 프롬프트 번호를 입력해주세요.")
        return None
    return prompts[int(answer) - 1]


def show_detail(prompts):
    print("\n=== 프롬프트 상세 보기 ===")
    prompt = choose_prompt(prompts)
    if prompt is None:
        return
    print(f'제목: {prompt["title"]}')
    print(f'카테고리: {prompt["category"]}')
    print(f'즐겨찾기: {"⭐" if prompt["favorite"] else "아니요"}')
    print("내용:")
    print(prompt["content"])


def show_menu():
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("0. 종료")


def main():
    prompts = load_sample_prompts()
    while True:
        show_menu()
        choice = input("선택: ").strip()
        if choice == "0":
            print("프로그램을 종료합니다.")
            break
        if choice == "1":
            add_prompt(prompts)
        elif choice == "2":
            show_list(prompts)
        elif choice == "3":
            show_category(prompts)
        elif choice == "4":
            search_prompt(prompts)
        elif choice == "5":
            show_detail(prompts)
        else:
            print("올바른 메뉴 번호를 입력해주세요.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\n프로그램을 종료합니다.")
