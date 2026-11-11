# PyTutor 3.0 — Final FYP Presentation Script

**Target:** 25 minutes main line (slides 1–23) + 1:35 buffer · Q&A after.
**Rules baked into this script:** every number is said with its boundary; no claim is upgraded on stage.
**【SAY】** = 可直接照读的英文原话 · *斜体中文* = 动作与节奏提示，不要读出来。

---

## Timing at a glance

| # | Slide | Time | Clock |
|---|---|---|---|
| 1 | Cover | 0:20 | 0:20 |
| 2 | Same mistake, three feedbacks | 1:10 | 1:30 |
| 3 | Gap / RQ / O1–O4 | 1:10 | 2:40 |
| 4 | Related work | 0:45 | 3:25 |
| 5 | Methodology | 1:05 | 4:30 |
| 6 | Architecture | 1:20 | 5:50 |
| 7 | Multi-stage decisions | 0:55 | 6:45 |
| 8 | Three-layer diagnosis | 1:15 | 8:00 |
| 9 | AST evidence | 1:05 | 9:05 |
| 10 | Pedagogical control | 1:15 | 10:20 |
| 11 | Profile + teacher | 1:00 | 11:20 |
| 12 | Engineering boundaries | 0:55 | 12:15 |
| 13 | Four screens | 0:30 | 12:45 |
| **14** | **Live demo** | **2:30** | **15:15** |
| 15 | Evaluation design | 1:00 | 16:15 |
| 16 | Diagnosis results | 1:15 | 17:30 |
| 17 | Retrieval | 1:00 | 18:30 |
| 18 | Response quality | 1:05 | 19:35 |
| 19 | Ablation status | 0:50 | 20:25 |
| 20 | Validity threats | 0:55 | 21:20 |
| 21 | Contributions | 0:50 | 22:10 |
| 22 | Future work | 0:40 | 22:50 |
| 23 | Conclusion | 0:35 | 23:25 |

> **Checkpoint discipline:** if you are past **8:00** at slide 9, or past **15:15** after the demo, drop slides 4 and 19 to one sentence each and merge 20 into 21.

---

## 01 · INTRODUCTION

### Slide 1 — Cover · 0:20

**【SAY】**
Good morning. My name is [name], and this is PyTutor 3.0 — a misconception-aware AI tutoring system for novice Python learners.

Over the next twenty-five minutes I'll show three things: what I built, how it decides what to tell a student, and — just as importantly — where the evidence stops.

*中文提示：不要从头念标题栏。说完最后一句停半秒，再切页。*

---

### Slide 2 — The same mistake, three kinds of feedback · 1:10

**【SAY】**
Let me start with one line of code that most beginners write at least once.

*（指代码块）* They create a list, call append, and assign the result to `new`. Then they print it. The output is `None`.

Three systems see exactly this submission.

An automated grader says: wrong answer, one of four tests passed. The learner receives a **verdict**.

A general-purpose LLM says: here is the corrected code. The learner receives an **answer** — and can copy it without understanding anything.

PyTutor says: misconception M3 — `append()` returns `None`, at line 2, and here is a level-one hint. The learner receives a **reason and a next step**.

*（停顿，降速）* The difference is not answer quality. It is whether the next action belongs to the learner or to the machine.

Automated grading and LLMs are both useful. Neither of them is a tutoring loop.

*中文提示：三栏按左中右顺序指，语速一致；最后一句是全场的主题句，说慢。*

---

### Slide 3 — Research gap, RQ, objectives · 1:10

**【SAY】**
The field already has three strong pieces.

**Automated assessment** scales to thousands of submissions, but its feedback stops at pass or fail. **LLM tutoring** gives fluent natural-language help, but it leaks answers and its output is unstable. **Intelligent tutoring systems** have real pedagogy and a learner model, but they are data- and authoring-heavy.

So the gap is not any single component. It is the **integration for novices**: interpretable diagnosis, scaffolded hints, and long-term tracking, in one workflow that can actually be verified.

That gives the research question: *can a Python tutoring system combine diagnosis, pedagogical control, and learner tracking in one verifiable workflow?*

I break that into four objectives — interpretable diagnosis, pedagogical control, learner adaptation, and verifiable engineering. These four come back at the end, one-to-one, as the four contributions.

*中文提示：三块短板各一句，不要展开；O1–O4 用手指数过去，不要逐条读小字。*

---

### Slide 4 — Related work and design position · 0:45

**【SAY】**
I place this work in four traditions. VanLehn on what tutoring actually buys over other instruction. Sorva on notional machines — how novices build a runtime model of code. Hevner on design science, which is the method I follow. Lewis and colleagues on retrieval-augmented generation. And Corbett and Anderson on knowledge tracing, which is where the profile design comes from.

But the **design position** is what matters here.

*（指底部横条）* I do not propose a new model. I propose a **constrained, inspectable pipeline** with evidence at each decision point.

*中文提示：这是唯一可以整段砍掉的一页。若时间紧，只念底部设计立场那一句，20 秒过。*

---

## 02 · METHOD & SYSTEM

### Slide 5 — Methodology · 1:05

**【SAY】**
The method is design science: problem, artifact, evaluation, iteration — three iterations, from a 2.0 diagnosis engine, to 3.0 with AST diagnosis and the learner profile, to an engineering closure pass.

But the part I want to defend is the **evaluation protocol** on the right.

Same-set and held-out results are both reported and **never mixed** into one number. Offline experiments and paid-API experiments are separated. Annotation was done by a single author — I declare that rather than hide it. And there is **no human learning study** — that is declared as a limitation, not quietly omitted.

I also use a fixed status vocabulary throughout: *implemented*, *enabled*, *verified*. A component can be implemented without being verified, and the slides will say which.

Every number in this deck is traceable to a result file or a test command.

---

### Slide 6 — Architecture · 1:20

**【SAY】**
*（从左往右划一条线）* The runtime path is: the student submits a question or code, the system classifies intent, retrieves supporting context, selects a teaching strategy, calls the model to generate language, and returns feedback — which then feeds back into the profile as evidence.

*（指 SAFeTY 条）* What matters is what sits **around** that model call. Execution goes through a sandbox with an environment whitelist, a ten-second timeout and a hundred-kilobyte output cap. Retrieval is ChromaDB with a TF-IDF fallback. Orchestration is a LangGraph agent. And the hint level plus profile update are computed outside the model and stored with the message.

*（指右侧 STACK 列）* The stack is deliberately conventional: Next.js and Monaco on the front, FastAPI and SQLAlchemy async on the back, DeepSeek through LiteLLM, DashScope embeddings.

*（指最下条）* One deployment note I'll come back to: the same codebase behaves differently by environment, because capability is **enforced**, not assumed.

The line I'd like you to remember from this slide: **the LLM writes language. Diagnosis, strategy and evidence live outside it.**

---

### Slide 7 — Multi-stage decisions · 0:55

**【SAY】**
So how does one submission turn into one response? Three explicit decisions.

First, **question type**: concept, debug, or exercise. Second, **retrieval strategy**: RAG, structured database, or none. Third, **response strategy**: explain, hint, or recommend.

Each produces a **decision trace** — selected branch, retrieved evidence, pedagogical strategy, response constraint.

That is not documentation for its own sake. Because each stage is explicit, each stage can be **logged, unit-tested, replaced behind a feature flag, and rolled back independently**.

No single prompt decides everything. Behaviour here is a composition of inspectable choices.

---

### Slide 8 — Three-layer diagnosis · 1:15

**【SAY】**
Diagnosis is the core mechanism, and it runs as a **chain**, not a vote.

**Layer one, regex rules.** Known patterns, under a millisecond, no network. Confidence 0.85. Its limit: syntax it has not seen.

**Layer two, AST analysis.** Structural facts plus line evidence, around 0.2 milliseconds, local and deterministic. Its limit: intent-level mistakes.

**Layer three, the LLM.** Unseen variants only, around 500 milliseconds. Its risk: output is not deterministic.

If layer one doesn't match, we fall to layer two. If structure doesn't settle it, we call the model. **The chain degrades; it never votes.**

*（指右下）* Two boundaries I want to state before questions come. Why not LLM-only — three reasons: latency, cost, determinism, plus an evidence trail the student can read. And the confidence value is a **ranking and gating score**, not a calibrated probability. I'll show what that rules out on the appendix slide.

---

### Slide 9 — AST evidence · 1:05

**【SAY】**
*（指代码四段）* Three of these four snippets are bugs. The first is M3 — assigning the return value of an in-place method. The second is M1 — assignment inside a condition. The third is M4 — using the index where the value was meant.

The fourth is clean code. It gets **no label**. That is precision shown in public.

*（指中间特征列）* What the analyser extracts is structural: assignment versus comparison, in-place method return values, index versus value in iteration, block scope and indentation, `print` versus `return`.

*（指证据对象）* The output is the evidence object: misconception, line, confidence, and the strategy that follows from it — in this example, line 2, confidence 0.575, progressive hint.

Across 47 cases the mean is 0.20 milliseconds, max 0.53. And the analyser **never executes student code**.

Structure facts are cheap, auditable, and stable across runs. That is what makes the label defensible.

---

### Slide 10 — Pedagogical control · 1:15

**【SAY】**
Diagnosis alone doesn't teach. This slide is the teaching policy.

Five hint levels, from L1 to L5. L1 names the relevant Python concept — no code, no line. L2 points at a direction. L3 identifies the suspicious line. L4 gives a key fragment. L5 is the complete answer.

*（指 FIRST ATTEMPT POLICY）* And on the **first attempt**, the system may only use L1 or L2. Full solutions are gated behind repeated attempts or an explicit request from the student.

On top of that, seven strategies: clarification, progressive hint, concept explanation, debugging guidance, counterexample, summary reflection, and practice recommendation — chosen by rule. First time in a misconception gets a progressive hint. Repeated three times or more gets a concept explanation. Multiple failures get debugging guidance.

*（指最后一行的位置）* The important design choice: the hint level is a **system decision, not a prompt suggestion**. It is computed outside the model, written into message metadata, and can be audited afterwards.

A fluent answer cannot override the teaching policy.

---

### Slide 11 — Learner and class · 1:00

**【SAY】**
One interaction should leave a trace, or the system never adapts.

The profile has four parts: weak topics as a JSON array, recent misconceptions capped at ten, hint dependency as a low/medium/high **label**, and completed lessons deduplicated. Time decay keeps old failures from dominating the current strategy.

*（指右栏）* The teacher view reads the **same** event stream: misconception ranking across the class, weak-topic top ten, hint-dependency distribution, and a student list.

Two things follow. First, student and teacher views are not a second pipeline. Second, the misconception label is an **intermediate representation** — it drives hints, profile updates, and class analytics. It is not the end product.

---

### Slide 12 — Engineering boundaries · 0:55

**【SAY】**
Four boundaries that make the system testable rather than merely demonstrable.

**Sandbox** — one execution boundary for every entry point, not one code path with a check.
**Feature flags** — ten independent switches, so each mechanism can be compared and rolled back without a deploy.
**Degradation** — failure is explicit. Embeddings fall back to TF-IDF, an LLM failure produces a template reply, a judge failure removes the quality badge. Nothing silently pretends to work.
**Rewards and events** — server-side truth only. First pass is rewarded once, idempotently, and viewing the solution zeroes the score.

*（指最底一行）* As of today, the offline suite runs 272 tests, 12 deselected; the frontend production build passes; CI runs lint, tests and build.

Boundaries are what turn a demo into something an examiner can reproduce.

---

## 03 · SYSTEM EVIDENCE

### Slide 13 — Four screens · 0:30

**【SAY】**
Four screens, one loop. Submission with the diagnosis card. Hint progression from L1 to L2 to L3 on the same exercise. The learner profile. And the teacher dashboard.

*（每张只说一句，不解释 UI）* I'll show all four working in the demo next.

*中文提示：这一页只是画面索引，别展开。说完立刻切到演示。*

---

### Slide 14 — Live demo · 2:30

**【SAY】** — 六步，每步一句，不回到架构。

1. *（选题）* — I'll take the list exercise that produces M3.
2. *（写 bug）* — I'll write the bug on purpose: assign the result of `append`.
3. *（提交）* — The system returns the diagnosis: M3, with the line evidence.
4. *（要提示）* — I ask for a hint. It gives L1, then L2. **It does not give the answer.**
5. *（改对）* — I fix it and resubmit. Accepted, and the reward is granted once — not twice.
6. *（画像 + 教师端）* — And here is the same event in two views: the student's profile, and the teacher's class dashboard.

**【SAY】** 收尾一行：That is the research pipeline in motion: input, diagnosis, guidance, evidence.

*中文提示：演示中不要排障。任何异常——网络、API、判题——立刻切到 90 秒预录视频，并说一句 "I have a recording of the same six steps." 绝不在台上 debug。*

---

## 04 · EVALUATION & RESULTS

### Slide 15 — Evaluation design · 1:00

**【SAY】**
Before the numbers, what was measured — and what was not.

**Datasets:** 47 misconception cases and 22 clean submissions in the same set. A separate 30-case held-out set with 15 clean. Thirty RAG queries plus five unanswerable. Ten teaching cases for the multi-judge. Ten seeds for faithfulness. No overlap between same-set and held-out.

**Metrics:** exact match, macro-F1 and false-positive rate for diagnosis; Hit@5, Recall@5, MRR and context tokens for retrieval; mean score, revision rate and Fleiss κ for response quality; faithfulness as C1 versus C2 with paired confidence intervals.

**Protocol:** offline and API-dependent paths separated, the held-out set written **after** the rules, single-author annotation declared, and no participant study.

*（指红条）* Deliberately **not** measured: learning gain, human–judge agreement, calibrated confidence, production security.

The protocol is part of the contribution. It defines where a claim stops.

---

### Slide 16 — Diagnosis results · 1:15

**【SAY】**
*（指左半）* Same set: 47 of 47 exact match, macro-F1 of 1.000, zero false positives on 22 clean submissions, mean latency 0.20 milliseconds.

That number is an **upper bound** — and it is labelled as one, because the rules were written against these cases.

*（指右半，降速）* So I also wrote a held-out set afterwards, 30 cases and 15 clean. Result: 25 of 30, 83.3 percent exact match, macro-F1 0.883, and **zero** false positives on held-out clean code.

*（指 residUAL GAPS）* The residual gaps are honest and specific: M5 recall 0.25 — range boundaries; M6 recall 0.50 — print versus return. Both are ambiguous in natural language, and both are visible in the error analysis rather than averaged away.

The gap between the two conditions is 16.7 percentage points. I report both, side by side, never as one number.

*中文提示：主动报 M5/M6 的短板，比被问出来强。这一页评委最可能追问的就是 47/47。*

---

### Slide 17 — Retrieval · 1:00

**【SAY】**
Retrieval compares TF-IDF against semantic vectors on 30 answerable queries.

Vector retrieval wins where it should: Hit@5 goes from 0.900 to 0.933, Recall@5 from 0.407 to 0.501. But it **loses slightly** on MRR, 0.890 against 0.900 — so the top-ranked result is not more often correct. And it costs 635 milliseconds per query against 0.1 for TF-IDF.

So: semantic retrieval buys recall, at a latency and token cost. That is the honest summary.

*（指右下两块）* Two limits I want to state myself. First, Hybrid currently returns **identical** numbers to vector, because the hybrid weighting flag is off — that is not evidence that fusion helps, and I don't claim it. Second, all five unanswerable queries still returned results: **the retriever cannot abstain**. That is future work, not a hidden assumption.

---

### Slide 18 — Response quality · 1:05

**【SAY】**
Two experiments, and one of them is negative.

*（指左）* A three-judge pipeline over ten cases: mean score 2.4 out of 5, revision rate 9 out of 10, Fleiss κ of 0.405. So the judges agree moderately, and the pipeline reliably **flags** responses that need revision. But there is no human reference, so κ is inter-judge only — it does not tell you the judges are right.

*（指右）* The second experiment is the negative one. I hypothesised that adding AST evidence to the prompt would improve faithfulness. I ran it twice, with paired confidence intervals. In both runs, the version **with** AST evidence was not better — and the intervals cross zero.

So the hypothesis is not supported. I report it as a negative result: not hidden, not reframed.

A negative result is still a result. It constrains what the system may claim.

*中文提示：这一页的语气要平。负结果说得越干脆，前面所有正面数字越可信。*

---

### Slide 19 — Ablation status · 0:50

**【SAY】**
Not every comparison has the same status, so I label them.

**Completed:** AST versus regex channel offline; TF-IDF versus vector on 30 queries; same-set versus held-out diagnosis; sandbox boundary and reward idempotency tests.

**Partial:** faithfulness C1 versus C2 — two runs, small n; feature-flag ablations at unit level only; judge rubric revision with no human anchor.

**Not yet run:** a general-purpose assistant baseline, a participant learning-gain study, probability calibration, and blind human rating.

*（指最底）* I claim **no baseline comparison**, because none was run. The column labels exist so the deck cannot be over-read.

---

## 05 · REFLECTION & CONCLUSION

### Slide 20 — Validity threats · 0:55

**【SAY】**
Four standard threats, each with what was done about it.

**Internal validity:** same-set results are optimistic — handled by a separately written held-out set and by not tuning on it.

**External validity:** 30 plus 15 held-out cases, annotated by one author — reported as an estimate, with no population claim.

**Construct validity:** confidence is heuristic, not calibrated — so it is used for ranking and gating only, and no ECE or Brier score is reported.

**Conclusion validity:** no participant study and no blind human rating — so claims stay at component-level offline evidence.

Naming the threat is part of the method, not an apology.

---

### Slide 21 — Contributions · 0:50

**【SAY】**
Four contributions, one per objective.

**One:** interpretable diagnosis — regex, AST and LLM, with evidence, confidence, and line-level facts. 47 of 47 same-set, 25 of 30 held-out, zero false positives in both conditions.

**Two:** pedagogical control — seven strategies and five hint levels, enforced outside the model. First attempt limited to L1–L2, strategy stored in metadata.

**Three:** learner adaptation — profile, time decay, misconception history, and teacher analytics.

**Four:** verifiable engineering — one sandbox boundary, ten feature flags, offline evaluation, CI, 272 tests.

*（指底部一句）* Positioning: a runnable, evaluable, explainable tutoring workflow — not another LLM interface.

*中文提示：**绝对不要**说 "improves learning outcomes"。说 workflow、pipeline、verifiable。*

---

### Slide 22 — Future work · 0:40

**【SAY】**
Each future item is blocked by a **resource**, not by an engineering unknown.

Calibrating confidence needs at least 200 independently labelled examples. A second annotator needs a second human — then I can re-label the held-out 45 and report agreement. Human evaluation needs ethics approval and raters. Retriever abstention needs calibrated scores before a threshold is meaningful.

Knowing *why* something is not done yet is more useful than promising it will be.

---

### Slide 23 — Conclusion · 0:35

**【SAY】**
To close.

PyTutor is not a smarter chatbot. It is a **constrained tutoring workflow** whose claims stop where the evidence stops.

*（三条，各一句，平速）*
Diagnosis is structural and inspectable.
Teaching is a system decision, not a prompt.
And evidence is reported together with its boundary.

Thank you — I'm happy to take questions.

*中文提示：说完"Thank you"就停住，不再补功能点。等评委开口。*

---

## Q&A 准备

### 三句护栏（先背熟，超纲就回到这里）

| 主题 | 标准回答 |
|---|---|
| Same-set vs held-out | "Same-set is 47/47; the held-out set I wrote separately is 25/30 with zero false positives, and the gap is M5/M6." |
| Retrieval | "Vector beats TF-IDF on Hit@5 and Recall@5, loses slightly on MRR, and costs 635 ms per query." |
| Scope | "The engineering loop is verified offline; learning gain and human quality ratings are not measured yet." |

超出这三句的，标准句式：**"Not measured — here is what it would take."**

---

### 高频问题与答法

**Q1. 为什么不能直接用 ChatGPT / DeepSeek？为什么要这么复杂的管线？**
> A general model optimises for a good answer. A tutoring system has to optimise for the *next action by the learner*. That requires three things a single prompt cannot guarantee: a stable diagnosis with a line number, a teaching policy that survives a fluent model, and a trace you can audit afterwards. My measurements show what the model alone costs — the LLM layer is around 500 ms and non-deterministic; the structural layers are 0.2 ms and reproducible. The pipeline exists to keep the deterministic part deterministic.

**Q2. 47/47 是不是过拟合？**
> Yes, in the sense that it is an upper bound — the rules were written against those cases, and I label it that way on the slide. That is exactly why I wrote a separate held-out set after the rules were frozen: 25/30, macro-F1 0.883, zero false positives. The number I would defend is 83.3 percent as an *estimate*, with single-author annotation as its main weakness.

**Q3. 83.3% 够用吗？**
> For a component in a workflow that also tells the student the line and the concept, it is useful. For an automatic grading system it would not be enough. The two failures are M5 and M6, both of which are ambiguous even to a human reader without running the code — and both are visible in the error analysis rather than averaged into the total.

**Q4. 你怎么保证提示是在教，而不是直接告诉答案？**
> Because the hint level is computed outside the model and enforced. On the first encounter the policy permits only L1 or L2 — concept or direction, no line number. L5 requires repeated attempts or an explicit request. The level is written into message metadata, so it can be audited after the fact rather than inferred from the text.

**Q5. 只有 8 类误区，够吗？**
> The catalogue is data — `misconceptions.json`. Adding a class does not change the engine. M1–M8 were chosen because they are high-frequency in introductory Python *and* structurally detectable. The honest limitation is coverage, not architecture.

**Q6. 置信度 0.575 是什么？是概率吗？**
> No. It is a ranking and gating score: it orders competing diagnoses and suppresses weak evidence. The weights are heuristic. A real probability needs at least 200 independently labelled examples and a fitted model, and then I would report ECE and Brier. Until then I don't call it a probability.

**Q7. Hybrid 检索为什么没有提升？**
> Because the hybrid weighting flag is off in the current configuration — so it computes the same thing as vector and returns identical numbers. I report that as a configuration fact, not as evidence about fusion. Turning it on is a one-flag change; measuring it properly is the next experiment.

**Q8. 部署版的判题不可用，这是不是失败？**
> It is designed behaviour. Judging requires an isolated sandbox. In production, if Docker is unavailable, the system refuses to judge rather than executing student code on the host. An "unavailable" verdict is a safety feature. That is also why the live demo runs locally or in Docker Compose, not on the deployed instance.

**Q9. 你最想改进的一点是什么？**
> A second annotator on the held-out set. Every number in this deck rests on single-author labels, and re-labelling 45 cases with a second person would let me report agreement and quantify exactly how much of the 83.3 percent is real. It is the cheapest fix with the largest effect on credibility.

**Q10. 安全方面做了哪些？**
> A sandbox with an environment whitelist, ten-second timeout, 100 KB output cap, blocked builtins and imports, a fresh temporary directory and a unique container per run. What I did **not** do: seccomp or AppArmor profiles, and a formal security audit. I describe the boundary rather than claim production-grade security.

**Q11. AI 组件怎么测试？**
> Three layers. Structural layers are unit-tested deterministically — the AST analyser never executes code, so results are exact. The LLM layers are tested offline with CLI commands and result files, not with flaky live calls in CI. And every mechanism sits behind a feature flag, so it can be disabled and compared instead of trusted.

**Q12. 有没有和别的系统做过对比？**
> No baseline comparison was run, and I say so on the ablation slide. A general-purpose assistant baseline is listed under "not yet run" together with learning-gain study and blind human rating. Claiming a comparison I did not run would be the single easiest way to lose credibility here.

**Q13. 学习效果有没有提升？**
> Not measured. There was no participant study and no pre/post test, so I can't claim learning gain. What is verified is the engineering loop: diagnosis accuracy, retrieval quality, policy enforcement and reproducibility. The next step would be a controlled study with pre/post tests, which needs ethics approval and a cohort.

**Q14. 如果时间更多，你会重做哪一部分？**
> The annotation. The architecture is stable and the numbers are reproducible; what limits every claim is that one person wrote the labels. A second annotator plus a calibration set would upgrade the confidence model from heuristic to measured, and would give the held-out estimate an error bar.

---

### 保守回答模板（不确定时）

- "That specific number isn't in my result set — what I can tell you is …"
- "I didn't measure that. What it would take is …"
- "That's a design choice, and the reason is … — but I haven't validated it against an alternative."
- **不要**现场推测数字；**不要**说 "probably" 来形容结果。

---

## 排练清单

- [ ] 计时跑三遍，检查 **8:00 / 15:15 / 23:25** 三个检查点
- [ ] 演示至少完整跑五次；准备预录视频并确认能播放
- [ ] 替换封面姓名、导师、学院；替换第 13 页四张截图
- [ ] 第 24 页参考文献核对卷期页码
- [ ] 背熟三句护栏 + Q1 / Q2 / Q3 / Q9
- [ ] 确认现场：投影比例 16:9、PDF 备份、网络、Docker 是否可用
- [ ] 若判题不可用：**不要**现场排查，直接翻到附录 29 页说明设计边界
