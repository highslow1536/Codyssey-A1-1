# 나만의 프롬프트 관리

Python 3.10 이상에서 실행하는 콘솔 기반 프롬프트 관리 프로그램입니다. 외부 라이브러리는 필요하지 않습니다.

## 환경 확인

```bash
python3 --version
git --version
python3 hello.py
```

`hello.py`는 개발 환경 확인용으로 `Hello`를 출력합니다.

## 실행

```bash
python3 prompt_manager.py
```

Windows에서 `python3` 명령이 없다면 `python`으로 바꾸어 실행하세요.

## 기능

메뉴 번호를 입력하여 다음 기능을 사용할 수 있습니다.

| 번호 | 기능 |
| --- | --- |
| 1 | 제목, 내용, 카테고리를 입력하여 프롬프트 추가 |
| 2 | 전체 목록과 즐겨찾기 표시 |
| 3 | 카테고리별 조회 |
| 4 | 제목 또는 내용에서 키워드 검색 |
| 5 | 전체 내용 상세 보기 |
| 6 | 즐겨찾기 추가 또는 해제 |
| 7 | 즐겨찾기 목록 |
| 0 | 종료 |

카테고리 기본 목록은 **텍스트 생성, 이미지 생성, 영상 생성, 페르소나, 자동화, 기타**입니다. 추가할 때 직접 카테고리 이름을 입력할 수도 있습니다. 실행 중 추가한 데이터와 즐겨찾기 상태는 메모리에 유지되며, 종료 후에는 초기화됩니다.

## 기본 데이터

[`sample_prompts.py`](sample_prompts.py)에 시연용 프롬프트 3개가 등록되어 있습니다. **이전 미션에서 작성한 실제 프롬프트가 제공되지 않아 예시로 채웠습니다. 제출 전 자신의 프롬프트 3개 이상으로 교체해야 해당 조건을 충족합니다.** 각 항목은 `title`, `content`, `category`, `favorite` 값을 포함합니다.

## Git 기록과 제출

목록 기능은 `feature/prompt-list` 브랜치에서 작성하고 `main`으로 병합했습니다. 다음 명령으로 기록을 확인할 수 있습니다.

```bash
git log --oneline --graph --all
```

GitHub 저장소: https://github.com/highslow1536/Codyssey-A1-1

현재 프로젝트는 `origin`에 연결되어 있습니다. 이후 변경사항은 다음 명령으로 업로드하고 동기화할 수 있습니다.

```bash
git push origin main
git pull origin main
```

제출할 때 GitHub 저장소 URL과 개발 환경 화면(VSCode Python 확장, `python3 --version`, `git --version`, `git config --list`), 프로그램 실행 화면(메뉴, 추가, 목록, 검색), `git log --oneline --graph --all` 화면을 캡처하세요. VSCode의 GitHub 계정 로그인은 본인 계정에서 확인해야 합니다.
