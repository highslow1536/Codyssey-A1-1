"""콘솔 프롬프트 관리 프로그램."""

import json
import re
from pathlib import Path

from sample_prompts import load_sample_prompts

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]
DATA_FILE = Path("prompts.json")
EXPORT_DIR = Path("exports")


def read_nonempty(label):
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print("빈 값은 입력할 수 없습니다. 다시 입력해주세요.")


def choose_category(prompts, allow_custom=False, current=None):
    categories = list(dict.fromkeys(CATEGORIES + [p["category"] for p in prompts]))
    print("카테고리 선택:")
    for number, category in enumerate(categories, 1):
        print(f"{number}. {category}")
    if allow_custom:
        print("직접 입력하려면 카테고리 이름을 입력하세요.")
    while True:
        answer = input("선택 (Enter: 현재 값 유지): ").strip() if current else read_nonempty("선택")
        if not answer and current:
            return current
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
    prompts.append({"title": title, "content": content, "category": category, "favorite": False, "view_count": 0})
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


def choose_prompt_index(prompts):
    answer = input("프롬프트 번호: ").strip()
    if not answer.isdecimal() or not 1 <= int(answer) <= len(prompts):
        print("올바른 프롬프트 번호를 입력해주세요.")
        return None
    return int(answer) - 1


def choose_prompt(prompts):
    index = choose_prompt_index(prompts)
    return prompts[index] if index is not None else None


def show_detail(prompts):
    print("\n=== 프롬프트 상세 보기 ===")
    prompt = choose_prompt(prompts)
    if prompt is None:
        return
    prompt["view_count"] += 1
    print(f'제목: {prompt["title"]}')
    print(f'카테고리: {prompt["category"]}')
    print(f'즐겨찾기: {"⭐" if prompt["favorite"] else "아니요"}')
    print(f'조회수: {prompt["view_count"]}')
    print("내용:")
    print(prompt["content"])


def toggle_favorite(prompts):
    print("\n=== 즐겨찾기 관리 ===")
    prompt = choose_prompt(prompts)
    if prompt is None:
        return
    prompt["favorite"] = not prompt["favorite"]
    action = "추가" if prompt["favorite"] else "해제"
    print(f'"{prompt["title"]}" 즐겨찾기를 {action}했습니다.')


def show_favorites(prompts):
    print("\n=== 즐겨찾기 목록 ===")
    found = 0
    for number, prompt in enumerate(prompts, 1):
        if prompt["favorite"]:
            print(f'{number}. [{prompt["category"]}] {prompt["title"]} ⭐')
            found += 1
    if found:
        print(f"총 {found}개의 즐겨찾기")
    else:
        print("즐겨찾기한 프롬프트가 없습니다.")


def save_json(prompts, path=DATA_FILE):
    try:
        path.write_text(json.dumps(prompts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError as error:
        print(f"저장하지 못했습니다: {error}")
        return
    print(f"{path} 파일에 {len(prompts)}개의 프롬프트를 저장했습니다.")


def load_json(prompts, path=DATA_FILE):
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"불러오지 못했습니다: {error}")
        return
    if not isinstance(loaded, list):
        print("올바른 프롬프트 목록 형식이 아닙니다.")
        return
    validated = []
    for item in loaded:
        if not isinstance(item, dict):
            print("올바른 프롬프트 항목 형식이 아닙니다.")
            return
        if any(not isinstance(item.get(key), str) or not item[key].strip()
               for key in ("title", "content", "category")):
            print("제목·내용·카테고리가 비어 있거나 문자열이 아닙니다.")
            return
        count = item.get("view_count", 0)
        if (not isinstance(item.get("favorite"), bool)
                or type(count) is not int or count < 0):
            print("즐겨찾기 또는 조회수 값이 올바르지 않습니다.")
            return
        validated.append({
            "title": item["title"], "content": item["content"],
            "category": item["category"], "favorite": item["favorite"],
            "view_count": count,
        })
    prompts[:] = validated
    print(f"{path} 파일에서 {len(prompts)}개의 프롬프트를 불러왔습니다.")


def export_markdown(prompts, directory=EXPORT_DIR):
    if not prompts:
        print("내보낼 프롬프트가 없습니다.")
        return
    groups = {}
    for number, prompt in enumerate(prompts, 1):
        groups.setdefault(prompt["category"], []).append((number, prompt))
    try:
        directory.mkdir(parents=True, exist_ok=True)
        for number, (category, entries) in enumerate(groups.items(), 1):
            safe_name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", category).strip(" .") or "category"
            path = directory / f"{number:02d}-{safe_name}.md"
            sections = [f"# {category}"]
            for prompt_number, prompt in entries:
                sections.append(
                    f'## {prompt_number}. {prompt["title"]}\n\n'
                    f'즐겨찾기: {"예" if prompt["favorite"] else "아니요"}  \n'
                    f'조회수: {prompt["view_count"]}\n\n{prompt["content"]}'
                )
            path.write_text(sections[0] + "\n\n" + "\n---\n\n".join(sections[1:]) + "\n", encoding="utf-8")
    except OSError as error:
        print(f"내보내지 못했습니다: {error}")
        return
    print(f"{len(groups)}개 카테고리를 {directory} 폴더에 내보냈습니다.")


def edit_prompt(prompts):
    print("\n=== 프롬프트 수정 ===")
    prompt = choose_prompt(prompts)
    if prompt is None:
        return
    title = input(f'새 제목 (Enter: {prompt["title"]} 유지): ').strip()
    content = input("새 내용 (Enter: 현재 내용 유지): ").strip()
    category = choose_category(prompts, allow_custom=True, current=prompt["category"])
    if title:
        prompt["title"] = title
    if content:
        prompt["content"] = content
    prompt["category"] = category
    print("프롬프트를 수정했습니다.")


def delete_prompt(prompts):
    print("\n=== 프롬프트 삭제 ===")
    index = choose_prompt_index(prompts)
    if index is None:
        return
    answer = input(f'"{prompts[index]["title"]}" 삭제를 확인하려면 y를 입력하세요: ').strip().lower()
    if answer == "y":
        removed = prompts.pop(index)
        print(f'"{removed["title"]}" 프롬프트를 삭제했습니다.')
    else:
        print("삭제를 취소했습니다.")


def show_top(prompts):
    print("\n=== 조회수 Top 5 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return
    ranked = sorted(enumerate(prompts, 1), key=lambda pair: -pair[1]["view_count"])
    for number, prompt in ranked[:5]:
        print(f'{number}. [{prompt["category"]}] {prompt["title"]} - 조회수 {prompt["view_count"]}')


def show_menu():
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("8. JSON 저장")
    print("9. JSON 불러오기")
    print("10. 카테고리별 Markdown 내보내기")
    print("11. 프롬프트 수정")
    print("12. 프롬프트 삭제")
    print("13. 조회수 Top 5")
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
        elif choice == "6":
            toggle_favorite(prompts)
        elif choice == "7":
            show_favorites(prompts)
        elif choice == "8":
            save_json(prompts)
        elif choice == "9":
            load_json(prompts)
        elif choice == "10":
            export_markdown(prompts)
        elif choice == "11":
            edit_prompt(prompts)
        elif choice == "12":
            delete_prompt(prompts)
        elif choice == "13":
            show_top(prompts)
        else:
            print("올바른 메뉴 번호를 입력해주세요.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\n프로그램을 종료합니다.")
