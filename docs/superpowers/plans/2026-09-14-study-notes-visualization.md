# Study Notes Visualization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Remove the Day 1–3 label and add relationship-driven learning diagrams to all 15 lecture pages without replacing their existing explanations.

**Architecture:** Keep the static HTML structure and shared theme. Add one small reusable visualization vocabulary to assets/seoyeon-journal.css, then annotate existing useful diagrams and insert only the missing flow, comparison, stack, and timeline blocks in each page.

**Tech Stack:** Static HTML5, shared CSS, existing vanilla JavaScript, Python standard-library regression checks

**Spec:** docs/superpowers/specs/2026-09-14-study-notes-visualization-design.md

## Global Constraints

- Cover lectures/00 through lectures/14: all 15 pages.
- Use relationship-matched flow, comparison, hierarchy, and timeline diagrams.
- Preserve existing explanations and quizzes.
- Remove Day 1–3 and Day 1-3 from the home card and machine-learning page.
- Add no external images, chart libraries, or JavaScript dependencies.
- Reuse existing flow, stackbox, compare-grid, and overview-grid structures before adding markup.
- Every learning diagram must contain text labels and remain readable in dark mode and at 320px width.
- Do not push until the user reviews the completed result.

---

## File Structure

- Modify: assets/seoyeon-journal.css — shared visual components and responsive behavior
- Modify: index.html — remove the machine-learning Day label
- Modify: lectures/00-python-basics/index.html through lectures/14-model-development/index.html — add or mark relationship diagrams
- Modify: lectures/13-ml-fundamentals/index.html — also remove two remaining Day labels
- Create: tests/test_learning_visuals.py — page coverage, visual count, label removal, and semantic checks

The HTML contract used by every task is:

    <div class="learning-viz viz-flow" role="img" aria-label="Short description">
      <div class="viz-node"><span>STEP 1</span><strong>Readable label</strong></div>
      <div class="viz-arrow" aria-hidden="true">→</div>
      <div class="viz-node is-accent"><span>STEP 2</span><strong>Readable label</strong></div>
    </div>

Existing diagrams keep their current classes and receive learning-viz, role="img", and a concise aria-label.

---

### Task 1: Shared visual language and Day-label cleanup

**Files:**
- Create: tests/test_learning_visuals.py
- Modify: assets/seoyeon-journal.css
- Modify: index.html:203
- Modify: lectures/13-ml-fundamentals/index.html:48,288

**Interfaces:**
- Produces: learning-viz marker; viz-flow, viz-compare, viz-stack, viz-timeline, viz-node, viz-arrow, viz-panel, viz-layer, and viz-step CSS classes
- Produces: page_minimums dictionary in tests/test_learning_visuals.py, extended by Tasks 2–7

- [ ] **Step 1: Write the failing shared-style and label test**

Create tests/test_learning_visuals.py:

    from html.parser import HTMLParser
    from pathlib import Path

    ROOT = Path(__file__).parents[1]
    CSS = (ROOT / "assets/seoyeon-journal.css").read_text(encoding="utf-8")
    PAGE_MINIMUMS = {}

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

- [ ] **Step 2: Run the test and verify RED**

Run:

    python3 tests/test_learning_visuals.py

Expected: FAIL because .learning-viz is absent and Day labels remain.

- [ ] **Step 3: Add the minimal shared CSS**

Append to assets/seoyeon-journal.css:

    .learning-viz { margin: 22px 0; }
    .viz-flow {
      display: flex;
      align-items: stretch;
      gap: 8px;
    }
    .viz-node, .viz-panel, .viz-layer, .viz-step {
      flex: 1;
      padding: 16px;
      border: 1px solid var(--border);
      border-radius: 14px;
      background: var(--panel2);
    }
    .viz-node span, .viz-layer span, .viz-step span {
      display: block;
      margin-bottom: 4px;
      color: var(--muted);
      font-size: 12.5px;
      font-weight: 750;
    }
    .viz-node strong, .viz-layer strong, .viz-step strong { display: block; }
    .viz-node.is-accent, .viz-layer.is-accent {
      border-color: color-mix(in srgb, var(--brand) 45%, var(--border));
      background: color-mix(in srgb, var(--brand) 10%, var(--panel2));
    }
    .viz-arrow { align-self: center; color: var(--muted); font-weight: 800; }
    .viz-compare { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 12px; }
    .viz-stack { display: grid; gap: 7px; }
    .viz-timeline { display: grid; gap: 10px; border-left: 3px solid var(--brand); padding-left: 18px; }
    @media (max-width: 680px) {
      .viz-flow { flex-direction: column; }
      .viz-flow .viz-arrow { transform: rotate(90deg); }
      .viz-compare { grid-template-columns: 1fr; }
    }

- [ ] **Step 4: Remove every requested Day label**

Change index.html heading to:

    <h3>머신러닝 및 딥러닝 이해</h3>

Change the machine-learning sidebar description to:

    <p class="sub">기초부터 트리·거리·딥러닝까지</p>

Change the machine-learning footer to:

    <footer class="pagefoot">데이터분석 및 AIOps · 머신러닝 및 딥러닝 이해 — 서연의 개인 복습 노트</footer>

- [ ] **Step 5: Run tests and commit**

Run:

    python3 tests/test_learning_visuals.py
    git diff --check

Expected: PASS.

Commit:

    git add assets/seoyeon-journal.css index.html lectures/13-ml-fundamentals/index.html tests/test_learning_visuals.py
    git commit -m "style: add learning visualization system"

---

### Task 2: Python and database pages

**Files:**
- Modify: tests/test_learning_visuals.py
- Modify: lectures/00-python-basics/index.html
- Modify: lectures/01-python-data-analysis/index.html
- Modify: lectures/02-smart-data/index.html

**Interfaces:**
- Consumes: learning-viz marker and viz-flow, viz-compare, viz-stack classes from Task 1
- Produces: three labeled diagrams per page

- [ ] **Step 1: Extend the page coverage test**

Set PAGE_MINIMUMS to:

    PAGE_MINIMUMS = {
        "lectures/00-python-basics/index.html": 3,
        "lectures/01-python-data-analysis/index.html": 3,
        "lectures/02-smart-data/index.html": 3,
    }

- [ ] **Step 2: Run the test and verify RED**

Run:

    python3 tests/test_learning_visuals.py

Expected: FAIL with 0/3 for the first uncovered page.

- [ ] **Step 3: Add three Python-basics diagrams**

Insert after each target section subtitle:

- s1 viz-flow: 입력 → 조건·반복 → 함수 → 출력
- s6 viz-compare: List 순서·중복, Set 고유값, Tuple 불변, Dict 키–값
- s13 viz-flow: 수집 → 정리 → 분석 → 시각화 → 해석

Use this exact node shape for the s1 flow, replacing only labels for the other two blocks:

    <div class="learning-viz viz-flow" role="img" aria-label="Python 프로그램이 입력을 받아 처리하고 결과를 출력하는 흐름">
      <div class="viz-node"><span>INPUT</span><strong>값 입력</strong></div>
      <div class="viz-arrow" aria-hidden="true">→</div>
      <div class="viz-node"><span>CONTROL</span><strong>조건·반복</strong></div>
      <div class="viz-arrow" aria-hidden="true">→</div>
      <div class="viz-node is-accent"><span>FUNCTION</span><strong>기능 묶기</strong></div>
      <div class="viz-arrow" aria-hidden="true">→</div>
      <div class="viz-node"><span>OUTPUT</span><strong>결과 출력</strong></div>
    </div>

- [ ] **Step 4: Add three Python-data-analysis diagrams**

- s1 viz-flow: 소스 코드 → Interpreter → Bytecode → Python VM
- s7 viz-compare: loc uses labels, iloc uses integer positions
- s11 viz-flow: 수집 → 검증 → 변환 → 분석 → 저장·공유

Each block must include learning-viz, role="img", and an aria-label that states the relationship.

- [ ] **Step 5: Add three Smart Data diagrams**

- s1 viz-stack: Application → DBMS → Storage/WAL
- s3 viz-flow: 요구사항 문장 → 개념 모델 → 논리 모델 → 물리 모델
- s10 viz-flow: 두 입력 → Join 조건 → 실행 알고리즘 → 결과 집합

Use viz-layer for the DB stack and viz-node for the two flows.

- [ ] **Step 6: Verify and commit**

Run:

    python3 tests/test_learning_visuals.py
    git diff --check

Expected: PASS.

Commit:

    git add tests/test_learning_visuals.py lectures/00-python-basics/index.html lectures/01-python-data-analysis/index.html lectures/02-smart-data/index.html
    git commit -m "docs: visualize Python and database concepts"

---

### Task 3: Statistics, prompt, and transformer pages

**Files:**
- Modify: tests/test_learning_visuals.py
- Modify: lectures/03-basic-statistics/index.html
- Modify: lectures/04-prompt-engineering/index.html
- Modify: lectures/05-llm-transformer/index.html

**Interfaces:**
- Consumes: learning-viz, viz-flow, viz-compare, viz-stack
- Produces: three labeled diagrams per page

- [ ] **Step 1: Add these three entries to PAGE_MINIMUMS**

    "lectures/03-basic-statistics/index.html": 3,
    "lectures/04-prompt-engineering/index.html": 3,
    "lectures/05-llm-transformer/index.html": 3,

- [ ] **Step 2: Run the test and verify RED**

Run python3 tests/test_learning_visuals.py.
Expected: FAIL with 0/3 for statistics.

- [ ] **Step 3: Visualize statistics**

- s3 viz-compare with three panels: 중심(평균·중앙값), 퍼짐(분산·표준편차), 형태(왜도·첨도)
- s4 viz-flow: 모집단 → 표본 추출 → 통계량 → 모집단 추론
- s5 viz-flow: H₀/H₁ 설정 → 유의수준 → 검정통계량·p-value → 기각 판단

Use short labels; keep formulas and existing explanatory paragraphs unchanged.

- [ ] **Step 4: Visualize prompt engineering**

- s3 viz-stack: Role → Context → Task → Constraints → Output Format
- s4 viz-flow: 목표 정의 → 예시·맥락 제공 → 응답 생성 → 평가 → Prompt 개선
- s6 viz-compare: Prompt Engineering, Context Engineering, Agent Workflow

The comparison panels must say what each method controls rather than claiming one replaces another.

- [ ] **Step 5: Visualize NLP and Transformer**

- s2 viz-flow: BoW/TF-IDF → Embedding → RNN/LSTM → Attention
- s4 viz-stack: Token+Position → Multi-Head Attention → Add&Norm → FFN → Output
- s7 viz-flow: Pre-training → Instruction Tuning → Preference Alignment → Inference

Add accessible labels that name the full progression.

- [ ] **Step 6: Verify and commit**

Run:

    python3 tests/test_learning_visuals.py
    git diff --check

Expected: PASS.

Commit the test and three pages with:

    git add tests/test_learning_visuals.py \
      lectures/03-statistics/index.html \
      lectures/04-prompt/index.html \
      lectures/05-transformer/index.html
    git commit -m "docs: visualize statistics and LLM concepts"

---

### Task 4: Spring, Agile/MSA, and sLLM pages

**Files:**
- Modify: tests/test_learning_visuals.py
- Modify: lectures/06-springboot-restapi/index.html
- Modify: lectures/07-agile-msa/index.html
- Modify: lectures/08-sllm-finetuning/index.html

**Interfaces:**
- Consumes: learning-viz, viz-flow, viz-compare, viz-stack, viz-timeline
- Produces: three or four labeled diagrams per page

- [ ] **Step 1: Add page minimums and verify RED**

Add:

    "lectures/06-springboot-restapi/index.html": 3,
    "lectures/07-agile-msa/index.html": 4,
    "lectures/08-sllm-finetuning/index.html": 3,

Run python3 tests/test_learning_visuals.py.
Expected: FAIL on the Spring page.

- [ ] **Step 2: Visualize Spring request processing**

- s1 viz-flow: .java → javac → .class bytecode → JVM
- s9 viz-flow: Client → Controller → Service → Repository → Database
- s17 viz-timeline: Transaction begin → Entity load/change → Dirty checking → Commit

- [ ] **Step 3: Visualize Agile and MSA**

- s1 viz-compare: Waterfall sequential delivery vs Agile iterative feedback
- s2 viz-flow with a loop label: Backlog → Sprint Planning → Development → Review → Retrospective → Backlog
- s5 viz-compare: Monolith single deployment vs MSA independent services
- s13 viz-flow: Commit → Test → Image Build → Deploy → Observe

- [ ] **Step 4: Visualize sLLM decisions**

- s1 viz-compare: external LLM API path vs self-hosted sLLM path
- s5 viz-stack: full fine-tuning → PEFT → LoRA, showing decreasing trainable parameters
- s12 viz-flow: dataset → train → evaluate → package → serve → monitor

- [ ] **Step 5: Verify and commit**

Run the learning-visual test and git diff --check.
Expected: PASS.

Commit:

    git add tests/test_learning_visuals.py lectures/06-springboot-restapi/index.html lectures/07-agile-msa/index.html lectures/08-sllm-finetuning/index.html
    git commit -m "docs: visualize backend and sLLM workflows"

---

### Task 5: Feature Engineering and Vue pages

**Files:**
- Modify: tests/test_learning_visuals.py
- Modify: lectures/09-feature-engineering/index.html
- Modify: lectures/10-vue-framework/index.html

**Interfaces:**
- Consumes: reusable visual classes plus Vue's existing .flow blocks
- Produces: three labeled Feature Engineering diagrams; accessibility annotations on at least four existing Vue diagrams

- [ ] **Step 1: Add page minimums and verify RED**

Add:

    "lectures/09-feature-engineering/index.html": 3,
    "lectures/10-vue-framework/index.html": 4,

Run python3 tests/test_learning_visuals.py.
Expected: FAIL for Feature Engineering.

- [ ] **Step 2: Visualize Feature Engineering**

- s1 viz-flow: Raw Data → Create → Transform → Select → Model
- s2 viz-compare: MCAR, MAR, MNAR with what the missingness depends on
- s10 viz-flow: offline Feature calculation → registry → online/offline store → training/serving

Add a clear train boundary label so population statistics are fitted only on Train.

- [ ] **Step 3: Reuse Vue's existing diagrams**

Add learning-viz, role="img", and aria-label to:

- #vue-flow .flow: Browser interaction → Vue state → rendering → API → state update
- #part-2 .flow: state → template → directives → user input
- #s10 .flow: parent state → Props → child → Emits → parent
- #s9 .flow: setup → mounted → updated → unmounted

Do not create duplicate Vue cards; the existing diagrams already satisfy the selected B strategy.

- [ ] **Step 4: Verify and commit**

Run the learning-visual test and git diff --check.
Expected: PASS.

Commit:

    git add tests/test_learning_visuals.py lectures/09-feature-engineering/index.html lectures/10-vue-framework/index.html
    git commit -m "docs: visualize feature engineering and Vue"

---

### Task 6: Docker and Kubernetes pages

**Files:**
- Modify: tests/test_learning_visuals.py
- Modify: lectures/11-containerization/index.html
- Modify: lectures/12-kubernetes/index.html

**Interfaces:**
- Consumes: existing .flow, .vflow, .stackbox components and learning-viz marker
- Produces: accessibility annotations on existing diagrams and one missing Kubernetes architecture stack

- [ ] **Step 1: Add page minimums and verify RED**

Add:

    "lectures/11-containerization/index.html": 4,
    "lectures/12-kubernetes/index.html": 4,

Run python3 tests/test_learning_visuals.py.
Expected: FAIL because existing flows are not marked.

- [ ] **Step 2: Mark four Docker diagrams**

Add learning-viz, role="img", and aria-label to:

- ch1 image → container flow
- ch1 container lifecycle .vflow
- ch3 host port ↔ published port ↔ container port flow
- ch10 db healthy → app → web Compose startup flow

Do not add new diagrams where the page already visualizes the same relationship.

- [ ] **Step 3: Mark and complete Kubernetes diagrams**

Mark:

- hero User → DNS/LB → Ingress → Service → Pod
- ch3 Deployment → ReplicaSet → Pod
- ch8 CoreDNS → Service → kube-proxy → CNI/Pod

In ch2 add a viz-stack labeled:

    Control Plane: API Server → Scheduler / Controller Manager → etcd
    Worker Node: kubelet → container runtime → kube-proxy → Pod

- [ ] **Step 4: Verify and commit**

Run the learning-visual test plus existing Docker and Kubernetes tests.
Expected: PASS.

Commit:

    git add tests/test_learning_visuals.py lectures/11-containerization/index.html lectures/12-kubernetes/index.html
    git commit -m "docs: improve Docker and Kubernetes diagrams"

---

### Task 7: Machine-learning and model-development pages

**Files:**
- Modify: tests/test_learning_visuals.py
- Modify: lectures/13-ml-fundamentals/index.html
- Modify: lectures/14-model-development/index.html

**Interfaces:**
- Consumes: existing .flow and .stackbox diagrams plus viz-compare and viz-timeline
- Produces: four labeled diagrams per page and no Day labels

- [ ] **Step 1: Add final page minimums and verify RED**

Add:

    "lectures/13-ml-fundamentals/index.html": 4,
    "lectures/14-model-development/index.html": 4,

Run python3 tests/test_learning_visuals.py.
Expected: FAIL because existing flows lack learning-viz.

- [ ] **Step 2: Mark and extend machine-learning diagrams**

Mark these existing flows:

- hero problem → data → learn → select → use
- ch9 sample → distance → K neighbors → vote
- ch14 input → weighted sum → activation → output
- ch16 forward → loss → backward → update

Add one viz-compare in ch3 only if no nearby table already clearly shows:

    Underfitting: train low / validation low
    Balanced: train high / validation high
    Overfitting: train high / validation low

The page must remain free of Day 1–3 and Day 1-3.

- [ ] **Step 3: Mark and extend model-development diagrams**

Mark the hero lifecycle flow. Add:

- ch5 viz-flow: split → fit preprocessing on Train → transform Validation/Test → fit model → final Test
- ch10 viz-compare: AUC ranks candidates vs Threshold triggers actions
- ch13 viz-timeline: data/prediction drift alert → label arrival → performance check → threshold/retrain/remodel

- [ ] **Step 4: Verify and commit**

Run:

    python3 tests/test_learning_visuals.py
    python3 tests/test_ml_fundamentals_page.py
    python3 tests/test_model_development_page.py
    git diff --check

Expected: PASS.

Commit:

    git add tests/test_learning_visuals.py lectures/13-ml-fundamentals/index.html lectures/14-model-development/index.html
    git commit -m "docs: visualize machine learning lifecycle"

---

### Task 8: Full-site verification and visual QA

**Files:**
- Modify only if verification reveals a concrete defect
- Verify: all tests/test_*.py and all 15 lecture pages

**Interfaces:**
- Consumes: completed 15-page visual system
- Produces: a clean, locally committed branch ready for user review

- [ ] **Step 1: Run every automated check**

Run:

    for test_file in tests/test_*.py; do python3 "$test_file" || exit 1; done
    node -e 'const fs=require("fs");const css=fs.readFileSync("assets/seoyeon-journal.css","utf8");if((css.match(/{/g)||[]).length!==(css.match(/}/g)||[]).length)throw Error("unbalanced CSS braces")'
    git diff --check

Expected: all tests pass, no CSS or whitespace errors.

- [ ] **Step 2: Check content preservation**

Run:

    git diff --word-diff=porcelain 5383e8c..HEAD -- lectures | rg '^-' | rg -v 'learning-viz|Day 1' || true

Review every reported deletion. Restore any removed explanatory sentence or quiz content.

- [ ] **Step 3: Preview representative layouts**

Run:

    python3 -m http.server 8000

Inspect the home page and pages 00, 02, 05, 06, 10, 11, 12, 13, and 14 at desktop 1440px, tablet 768px, and mobile 390px. Verify:

- no overlap or horizontal page overflow
- flow arrows turn vertical at narrow widths
- compare panels stack
- labels remain readable in light and dark mode
- tables and code retain their existing scrolling behavior

- [ ] **Step 4: Fix only confirmed defects, then rerun Step 1**

Do not add new components during QA. Fix the smallest selector or markup issue responsible for each observed defect.

- [ ] **Step 5: Report for user review**

Run:

    git status --short
    git log --oneline -8

Report the local commit range and preview URL. Do not push until the user explicitly asks.
