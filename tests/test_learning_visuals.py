from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).parents[1]
CSS = (ROOT / "assets/seoyeon-journal.css").read_text(encoding="utf-8")
PAGE_MINIMUMS = {
    "lectures/00-python-basics/index.html": 3,
    "lectures/01-python-data-analysis/index.html": 3,
    "lectures/02-smart-data/index.html": 3,
    "lectures/03-basic-statistics/index.html": 3,
    "lectures/04-prompt-engineering/index.html": 3,
    "lectures/05-llm-transformer/index.html": 3,
    "lectures/06-springboot-restapi/index.html": 3,
    "lectures/07-agile-msa/index.html": 4,
    "lectures/08-sllm-finetuning/index.html": 3,
    "lectures/09-feature-engineering/index.html": 3,
    "lectures/10-vue-framework/index.html": 4,
    "lectures/11-containerization/index.html": 4,
    "lectures/12-kubernetes/index.html": 4,
    "lectures/13-ml-fundamentals/index.html": 4,
    "lectures/14-model-development/index.html": 4,
}


class VisualParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.visuals = 0
        self.missing_labels = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if "learning-viz" in classes:
            self.visuals += 1
            if attrs.get("role") != "img" or not attrs.get("aria-label"):
                self.missing_labels.append(attrs)


for name in ("learning-viz", "viz-flow", "viz-compare", "viz-stack", "viz-timeline"):
    assert f".{name}" in CSS, name

combined = (
    (ROOT / "index.html").read_text(encoding="utf-8")
    + (ROOT / "lectures/13-ml-fundamentals/index.html").read_text(encoding="utf-8")
)
assert "Day 1–3" not in combined
assert "Day 1-3" not in combined

for relative, minimum in PAGE_MINIMUMS.items():
    parser = VisualParser()
    parser.feed((ROOT / relative).read_text(encoding="utf-8"))
    assert parser.visuals >= minimum, f"{relative}: {parser.visuals}/{minimum}"
    assert not parser.missing_labels, f"{relative}: diagram needs role and aria-label"

print("learning visualization checks passed")
