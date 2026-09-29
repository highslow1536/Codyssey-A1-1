"""보너스 기능의 데이터 보존과 메뉴 흐름을 확인한다."""

import copy
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import prompt_manager as app


def run_menu_action(function, prompts, answers):
    output = io.StringIO()
    with patch("builtins.input", side_effect=answers), redirect_stdout(output):
        function(prompts)
    return output.getvalue()


class BonusFeatureTests(unittest.TestCase):
    def test_json_round_trip_preserves_changes_and_korean(self):
        prompts = app.load_sample_prompts()
        prompts[0]["favorite"] = True
        prompts[0]["view_count"] = 3
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "prompts.json"
            with redirect_stdout(io.StringIO()):
                app.save_json(prompts, path)
            self.assertIn("블로그", path.read_text(encoding="utf-8"))
            restored = []
            with redirect_stdout(io.StringIO()):
                app.load_json(restored, path)
            self.assertEqual(restored, prompts)

    def test_bad_json_does_not_replace_current_prompts(self):
        prompts = app.load_sample_prompts()
        original = copy.deepcopy(prompts)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "prompts.json"
            path.write_text("{invalid", encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                app.load_json(prompts, path)
            self.assertEqual(prompts, original)
            path.write_text(json.dumps([{"title": "누락"}]), encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                app.load_json(prompts, path)
            self.assertEqual(prompts, original)

    def test_markdown_exports_every_category_with_safe_filenames(self):
        prompts = app.load_sample_prompts()
        prompts.append({"title": "제목", "content": "본문", "category": "새/분류", "favorite": True, "view_count": 2})
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp) / "exports"
            with redirect_stdout(io.StringIO()):
                app.export_markdown(prompts, directory)
            files = sorted(directory.glob("*.md"))
            self.assertEqual(len(files), 4)
            combined = "\n".join(path.read_text(encoding="utf-8") for path in files)
            for prompt in prompts:
                self.assertIn(prompt["title"], combined)
                self.assertIn(prompt["content"], combined)
            self.assertTrue(any("새_분류" in path.name for path in files))
            self.assertIn("조회수: 2", combined)

    def test_edit_and_delete_use_selected_number(self):
        first = app.load_sample_prompts()[0]
        second = copy.deepcopy(first)
        prompts = [first, second]
        run_menu_action(app.edit_prompt, prompts, ["2", "수정한 제목", "", "새 분류"])
        self.assertEqual(first["title"], "블로그 글 작성 도우미")
        self.assertEqual(second["title"], "수정한 제목")
        self.assertEqual(second["category"], "새 분류")
        run_menu_action(app.delete_prompt, prompts, ["2", "n"])
        self.assertEqual(len(prompts), 2)
        run_menu_action(app.delete_prompt, prompts, ["2", "y"])
        self.assertEqual(len(prompts), 1)
        self.assertIs(prompts[0], first)

    def test_detail_counts_views_and_top_sorts(self):
        prompts = app.load_sample_prompts()
        prompts[1]["view_count"] = 5
        output = run_menu_action(app.show_detail, prompts, ["1"])
        self.assertIn("조회수: 1", output)
        run_menu_action(app.show_detail, prompts, ["99"])
        self.assertEqual(prompts[0]["view_count"], 1)
        top = run_menu_action(app.show_top, prompts, [])
        self.assertLess(top.index(prompts[1]["title"]), top.index(prompts[0]["title"]))

    def test_menu_save_load_export_and_default_reset(self):
        script = Path(app.__file__).resolve()
        with tempfile.TemporaryDirectory() as temp:
            first = "1\n추가 항목\n추가 내용\n1\n5\n4\n6\n4\n8\n0\n"
            result = subprocess.run([sys.executable, str(script)], input=first, text=True,
                                    capture_output=True, cwd=temp, check=True)
            self.assertIn("프롬프트가 추가되었습니다", result.stdout)
            saved = json.loads((Path(temp) / "prompts.json").read_text(encoding="utf-8"))
            self.assertEqual(saved[3]["view_count"], 1)
            self.assertTrue(saved[3]["favorite"])

            second = "2\n9\n2\n10\n13\n0\n"
            result = subprocess.run([sys.executable, str(script)], input=second, text=True,
                                    capture_output=True, cwd=temp, check=True)
            self.assertIn("총 3개의 프롬프트", result.stdout)
            self.assertIn("총 4개의 프롬프트", result.stdout)
            self.assertIn("조회수 Top 5", result.stdout)
            self.assertEqual(len(list((Path(temp) / "exports").glob("*.md"))), 3)


if __name__ == "__main__":
    unittest.main()
