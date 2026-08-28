from html.parser import HTMLParser
from pathlib import Path


PAGE = Path(__file__).parents[1] / "lectures/11-containerization/index.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.nav_targets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("class") == "navlink":
            self.nav_targets.append(attrs.get("href", "").removeprefix("#"))


html = PAGE.read_text(encoding="utf-8")
parser = PageParser()
parser.feed(html)

assert "Docker 복습 노트" in html
assert {"operations", "practice", "confuse", "quiz"} <= parser.ids
assert all(target in parser.ids for target in parser.nav_targets)
assert html.count('    q: "') == 12

for required in (
    "Docker Desktop",
    "Linux VM",
    "docker ps -a",
    "프로세스 격리",
    "OS 수준 가상화",
    "docker0",
    "iptables",
    "liveness",
    "readiness",
    "startup",
    "Git push",
    "실습 체크리스트",
):
    assert required in html, required

for forbidden in ("녹취", "녹음", "197페이지짜리 원문", "Pre-study", "컨테이너 예습"):
    assert forbidden not in html, forbidden

print("containerization page checks passed")
