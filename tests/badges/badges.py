from os import getcwd, mkdir, remove
from os.path import join, isdir, isfile
from subprocess import Popen, PIPE
from anybadge import Badge
from tests.badges.errors import ProcessExecutionFailure, PyLintScoreFailure


class Badges:
    def __init__(self):
        cwd = getcwd()
        self.coverage_path = join(cwd, "tests", "codecoverage")
        self.index_path = join(self.coverage_path, "index.html")
        self.badge_paths = [
            join(self.coverage_path, "coverage.svg"),
            join(self.coverage_path, "pylint.svg"),
            join(self.coverage_path, "CodeStyle.svg"),
            join(self.coverage_path, "black.svg"),
            join(self.coverage_path, "bandit.svg"),
            join(self.coverage_path, "safety.svg"),
        ]
        self.lint_threshold = {2: "red", 4: "orange", 6: "yellow", 10: "green"}
        self.py_lint_command = "pylint src tests --rcfile=tox.ini"
        self.score_search_1 = "rated at "
        self.score_search_2 = "/"
        self.index_search = "</footer>"
        self.replace_text = (
            '    <td class="name left"><a href="coverage.svg">CoverageBadge</a></td>\n'
            '    <td class="name left"><a href="pylint.svg">pylint</a></td>\n'
            '    <td class="name left"><a href="CodeStyle.svg">CodeStyle</a></td>\n'
            '    <td class="name left"><a href="black.svg">black</a></td>\n'
            '    <td class="name left"><a href="safety.svg">safety</a></td>\n'
            '    <td class="name left"><a href="bandit.svg">bandit</a></td>\n'
            "</footer>"
        )

    def _check_badges(self):
        for path in self.badge_paths:
            if isfile(path):
                remove(path)

    def _check_folder(self):
        if isdir(self.coverage_path) is False:
            mkdir(self.coverage_path)

    def _cli(self, p_command):
        with Popen(
            [p_command], shell=True, universal_newlines=True, stdout=PIPE
        ) as process_obj:
            process_obj.wait()
            code = process_obj.returncode
            output = process_obj.stdout.read()
        return {"code": code, "output": output}

    def _index_content(self):
        with open(self.index_path, "r", encoding="utf-8") as file:
            content = file.read()
            new_content = content.replace(self.index_search, self.replace_text)
        file.close()
        return new_content

    def _lint_badge(self, p_score):
        badge = Badge("pylint", p_score, thresholds=self.lint_threshold)
        badge.write_badge("tests/codecoverage/pylint.svg")

    def _score(self, p_output):
        pre_index1 = p_output.find(self.score_search_1)
        index1 = pre_index1 + len(self.score_search_1)
        index2 = p_output.find(self.score_search_2)
        return p_output[index1:index2]

    def _write_index(self, p_content):
        with open(self.index_path, "w", encoding="utf-8") as file:
            file.write(p_content)
        file.close()

    def exe_black(self):
        self._check_badges()
        self._check_folder()
        badge = Badge("CodeFormat", "Black", default_color="#000000")
        badge.write_badge("tests/codecoverage/black.svg")

    def exe_code_style(self):
        badge = Badge("CodeStyle", "pass", default_color="#006400")
        badge.write_badge("tests/codecoverage/CodeStyle.svg")

    def exe_index(self):
        content = self._index_content()
        self._write_index(content)

    def exe_pylint(self):
        result = self._cli(self.py_lint_command)
        if result["code"] != 0:
            raise ProcessExecutionFailure("pylint", result["code"], result["output"])
        score = self._score(result["output"])
        if score != "10.00":
            raise PyLintScoreFailure(score)
        self._lint_badge(score)

    def exe_safety(self):
        badge1 = Badge("Bandit", "pass", default_color="#0000FF")
        badge1.write_badge("tests/codecoverage/bandit.svg")
        badge2 = Badge("Safety", "pass", default_color="#0000FF")
        badge2.write_badge("tests/codecoverage/safety.svg")
