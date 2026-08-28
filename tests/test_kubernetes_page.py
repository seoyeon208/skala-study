from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).parents[1]
PAGE = ROOT / "lectures/12-kubernetes/index.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.nav_targets = []
        self.part_groups = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and "navlink" in attrs.get("class", "").split():
            self.nav_targets.append(attrs.get("href", "").removeprefix("#"))
        if tag == "div" and "part-group" in attrs.get("class", "").split():
            self.part_groups += 1


assert PAGE.exists(), "Kubernetes 복습 페이지가 아직 없습니다"

html = PAGE.read_text(encoding="utf-8")
parser = PageParser()
parser.feed(html)

assert len(parser.ids) == len(set(parser.ids)), "중복된 HTML id가 있습니다"
assert parser.nav_targets and all(target in parser.ids for target in parser.nav_targets)
assert parser.part_groups == 6, "5개 학습 파트와 마무리 목차가 필요합니다"
assert html.count('    q: "') == 15, "상황형 복습 퀴즈는 15문항이어야 합니다"
assert 'href="lectures/12-kubernetes/index.html"' in (ROOT / "index.html").read_text(encoding="utf-8")
assert 'href="../12-kubernetes/index.html"' in (ROOT / "lectures/11-containerization/index.html").read_text(encoding="utf-8")

for forbidden in ("녹취", "녹음"):
    assert forbidden not in html, forbidden

print("kubernetes page checks passed")
