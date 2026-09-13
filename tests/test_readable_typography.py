import re
from pathlib import Path


ROOT = Path(__file__).parents[1]
CSS = (ROOT / "assets/seoyeon-journal.css").read_text(encoding="utf-8")


def font_size(selector):
    match = re.search(rf"{re.escape(selector)}\s*\{{([^}}]+)\}}", CSS)
    assert match, f"공통 가독성 규칙이 없습니다: {selector}"
    size = re.search(r"font-size:\s*([\d.]+)px", match.group(1))
    assert size, f"글자 크기가 없습니다: {selector}"
    return float(size.group(1))


pages = [ROOT / "index.html", *sorted((ROOT / "lectures").glob("*/index.html"))]
for page in pages:
    html = page.read_text(encoding="utf-8")
    assert "seoyeon-journal.css" in html, f"공통 CSS를 사용하지 않습니다: {page}"

assert font_size("html body") >= 17
assert font_size("html body .sidebar .navlink") >= 14
assert font_size("html body .sec p") >= 17
assert font_size("html body .ch-body p") >= 17
assert font_size("html body table") >= 15
assert font_size("html body pre code") >= 14
assert font_size("html body .quiz-opt") >= 15
assert font_size("html body .cp li") >= 16
assert font_size("html body .ch-title .sub") >= 14

print("global typography checks passed")
