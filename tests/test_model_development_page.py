from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).parents[1]
PAGE = ROOT / "lectures/14-model-development/index.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.nav_targets = []
        self.chapters = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        classes = attrs.get("class", "").split()
        if tag == "a" and "navlink" in classes:
            self.nav_targets.append(attrs.get("href", "").removeprefix("#"))
        if tag == "details" and "chapter" in classes:
            self.chapters += 1


assert PAGE.exists(), "모델 개발 및 최적화 페이지가 아직 없습니다"

html = PAGE.read_text(encoding="utf-8")
parser = PageParser()
parser.feed(html)

assert len(parser.ids) == len(set(parser.ids)), "중복된 HTML id가 있습니다"
assert parser.nav_targets and all(target in parser.ids for target in parser.nav_targets)
assert parser.chapters == 16, "전체 모델 개발 절차를 설명하는 16개 단원이 필요합니다"
assert html.count('    q: "') == 20, "상황형 복습 퀴즈는 20문항이어야 합니다"
assert 'href="lectures/14-model-development/index.html"' in (ROOT / "index.html").read_text(encoding="utf-8")

for required in (
    "Observation Window",
    "Train–Test Contamination",
    "PR-AUC",
    "Calibration",
    "Feature Importance·SHAP",
    "Model Drift",
    "Pipeline artifact",
    "pickle/joblib",
):
    assert required in html, required

for forbidden in ("녹취", "녹음"):
    assert forbidden not in html, forbidden

print("model development page checks passed")
