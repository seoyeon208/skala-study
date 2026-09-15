from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).parents[1]
PAGE = ROOT / "lectures/15-aws-cloud-essentials/index.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.nav_targets = []
        self.chapters = 0
        self.visuals = 0
        self.unlabelled_visuals = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and "navlink" in classes:
            self.nav_targets.append(attrs.get("href", "").removeprefix("#"))
        if tag == "details" and "chapter" in classes:
            self.chapters += 1
        if "learning-viz" in classes:
            self.visuals += 1
            if attrs.get("role") != "img" or not attrs.get("aria-label"):
                self.unlabelled_visuals += 1


assert PAGE.exists(), "AWS Cloud Essentials 페이지가 아직 없습니다"

html = PAGE.read_text(encoding="utf-8")
parser = PageParser()
parser.feed(html)

assert len(parser.ids) == len(set(parser.ids)), "중복된 HTML id가 있습니다"
assert parser.nav_targets and all(target in parser.ids for target in parser.nav_targets)
assert parser.chapters == 10, "AWS 핵심 흐름을 설명하는 10개 단원이 필요합니다"
assert parser.visuals >= 6, "관계를 보여 주는 시각화가 6개 이상 필요합니다"
assert parser.unlabelled_visuals == 0, "시각화에는 role과 aria-label이 필요합니다"
assert html.count('    q: "') == 15, "복습 퀴즈는 15문항이어야 합니다"
assert 'href="lectures/15-aws-cloud-essentials/index.html"' in (ROOT / "index.html").read_text(encoding="utf-8")

for forbidden in ("녹취", "녹음", "EKS는 SaaS"):
    assert forbidden not in html, forbidden

print("AWS Cloud Essentials page checks passed")
