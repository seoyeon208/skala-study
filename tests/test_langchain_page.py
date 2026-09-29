"""Check links, accessible diagrams and the Python examples without API calls."""
import ast
import json
import re
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "lectures/18-langchain/index.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.examples = [], [], []
        self.current = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag == "code" and attrs.get("class") == "language-python":
            self.current = ""

    def handle_data(self, data):
        if self.current is not None:
            self.current += data

    def handle_endtag(self, tag):
        if tag == "code" and self.current is not None:
            self.examples.append(self.current)
            self.current = None


html = PAGE.read_text()
page = PageParser()
page.feed(html)
assert len(page.ids) == len(set(page.ids)), "duplicate id"
for link in page.links:
    if link.startswith("#"):
        assert link[1:] in page.ids, link
    elif link and ":" not in link:
        assert (PAGE.parent / link).is_file(), link
assert 'href="lectures/18-langchain/index.html"' in (ROOT / "index.html").read_text()
assert not re.search("녹취|녹음|sk-[A-Za-z0-9]{20,}", html)
for index, example in enumerate(page.examples):
    ast.parse(example, filename=f"example-{index + 1}")

# Run the actual masking function from the published example, offline.
mask_example = next(s for s in page.examples if "def mask_phone" in s)
tree = ast.parse(mask_example)
offline_nodes = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.Assert))]
namespace = {"re": re}
exec(compile(ast.Module(body=offline_nodes, type_ignores=[]), "mask-example", "exec"), namespace)
assert namespace["mask_phone"]("일반 문장") == "일반 문장"
assert namespace["mask_phone"]("010123456789") == "010123456789"

questions = json.loads(html.split("const QUESTIONS=", 1)[1].split(";", 1)[0])
assert len(questions) == 20
for question in questions:
    assert len(question["opts"]) == 4
    assert 0 <= question["correct"] < len(question["opts"])
    assert question["explain"].strip()
print(f"LangChain page: links, {len(page.examples)} Python examples, masking and 20 questions checked")
