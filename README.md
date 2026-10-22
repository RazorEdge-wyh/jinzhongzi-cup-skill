# jinzhongzi-cup-skill

**An agent skill for Chinese college innovation & entrepreneurship competitions — evidence-led, format-correct, mechanically checkable.**

[中文说明](README.zh-CN.md) · [Design](docs/design.md) · [Format comparison](docs/format-comparison.md) · [Install](docs/install.md)

[![CI](https://github.com/RazorEdge-wyh/jinzhongzi-cup-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/RazorEdge-wyh/jinzhongzi-cup-skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v1.2.0-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-purple.svg)](https://agentskills.io/specification)

---

## Why this exists

Students preparing for competitions such as Hunan's **“金种子杯”**, **中国国际大学生创新大赛** or **“挑战杯”** face three recurring problems:

1. **Rules drift.** Score weights change between editions (market 30→20, finance 15→20, social value 10→15). Most online guides are outdated.
2. **Data gets invented.** LLM-generated proposals routinely contain plausible-but-fabricated numbers — a disqualifying risk in competitions that audit authenticity.
3. **Formats scatter.** The business plan, the 6-minute pitch and the paper are written separately, so numbers and scope contradict each other; GB/T 7714 citation details are easy to break.

This skill turns those three into **executable constraints and a linter**. It is not a pile of notes.

## What you get

| Capability | What it does |
|---|---|
| **Verified rule baseline** | Third-edition scoring (25/20/20/20/15), expert+AI 7:3 network review, ±15% deviation recheck, 12-minute final (6+6), eligibility, materials, awards, fund due-diligence |
| **Fact ledger** | Every claim goes into `evidence-ledger`; numbers are tagged `[实测]/[估算]/[待补]` before they enter a document |
| **Judging-dimension mapping** | “Scoring point ↔ section ↔ evidence” table, required deliverable for a BP |
| **De-AI writing discipline** | Narrative style, no label-style pseudo-headings, no process annotations in the body, restrained rhetoric |
| **Paper workflow** | IMRaD, GB/T 7714—2015 citation templates, three-line tables, significance letters, AI-use disclosure |
| **Submission linter** | Structure, empty phrases, unsourced numbers, annotation leaks, label-style, citation integrity, figure/table numbering, five-dimension coverage |
| **Word export** | `tools/md2docx.py` renders A4 / Chinese fonts / three-line tables / page-number footer, then convert to PDF |

## Quickstart

```bash
git clone https://github.com/RazorEdge-wyh/jinzhongzi-cup-skill.git
cd jinzhongzi-cup-skill
```

**DSH** (copies into `<project>/.dsh/skills`):

```powershell
.\tools\install.ps1 -Target dsh
```

**Claude Code / generic Agent Skills runtime**:

```powershell
.\tools\install.ps1 -Target claude   # ~/.claude/skills
.\tools\install.ps1 -Target agents   # ~/.agents/skills
```

Manual install: copy `skills/jinzhongzi-cup/` into your runtime's skills directory. The directory name must stay `jinzhongzi-cup`.

Then, in a new session:

```
/jinzhongzi-cup          # explicit
用 jinzhongzi-cup 把方案扩成 BP
帮我检查这份 BP 能不能过网评
把试验写成 GB/T 7714 格式的论文
```

## How it works

```
SKILL.md                      routing + iron rules + quality gate
├── references/01 … 09        lazy-loaded: rules, project facts, BP/pitch, paper, stats, AI review, sources
├── assets/templates/         6 fill-in templates (BP skeleton, Q&A bank, paper outline,
│                             experiment plan, evidence ledger, judging mapping)
└── scripts/check_submission.py   mechanical submission linter
```

1. **Progressive disclosure** — `SKILL.md` stays small; details load only when a task needs them.
2. **Evidence before prose** — claims are registered and tagged before writing.
3. **Mechanical check** — run the linter before every submission; it fails on missing sections and broken citations.
4. **Format alignment** — every format choice is traced in [docs/format-comparison.md](docs/format-comparison.md).

## Repository layout

```text
jinzhongzi-cup-skill/
├── skills/jinzhongzi-cup/     # the skill (Agent Skills spec)
│   ├── SKILL.md
│   ├── references/            # 9 reference docs
│   ├── assets/templates/      # 6 templates
│   └── scripts/check_submission.py
├── tools/                     # md2docx.py, validate_skill.py, install.ps1
├── tests/                     # unittest suite + fixtures
├── docs/                      # design, format comparison, install, writing style
├── examples/                  # sample outputs (clearly marked as examples)
├── .github/workflows/ci.yml   # tests + skill validation + linter fixtures
├── CHANGELOG.md · CONTRIBUTING.md · LICENSE
└── README.md / README.zh-CN.md
```

## Validation

```bash
python -m unittest discover -s tests -v      # 17 tests
python tools/validate_skill.py skills        # Agent Skills spec check
python skills/jinzhongzi-cup/scripts/check_submission.py --version
python skills/jinzhongzi-cup/scripts/check_submission.py --mapping
python skills/jinzhongzi-cup/scripts/check_submission.py tests/fixtures/plan_bad.md --kind plan  # exit 1
```

CI runs the same commands on Python 3.10 / 3.12 / 3.13.

## How it compares

| Project | Scope | What this skill does differently |
|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | Official skill examples | We follow the same spec/layout, but ship a **competition-specific** workflow with a linter and tests |
| [sevonsss/sevonsss-plan](https://github.com/sevonsss/sevonsss-plan) | Chinese BP skill, 60–80 page, ten chapters | We adopt its **de-AI writing discipline** and tri-class numbers; we target a 25–35 page BP because scoring here rewards structure and evidence, not length |
| [xwu43361-sys/innovation-proposal](https://github.com/xwu43361-sys/innovation-proposal) | Proposal skill with official 2026 rules | We adopt its **judging-dimension mapping** and add a runnable linter + tests |
| [fengmo11/awesome-paper-research-skills](https://github.com/fengmo11/awesome-paper-research-skills) | Curated index of paper skills | We are a single installable skill; format conventions (bilingual README, badges, CI, changelog) follow this ecosystem |
| [ustctug/ustcthesis](https://github.com/ustctug/ustcthesis) | LaTeX thesis template | We give GB/T 7714 rules and checklists instead of a template, so Word-based journal/graduation submissions stay covered |

Full comparison and per-item adopt/reject rationale: [docs/format-comparison.md](docs/format-comparison.md).

## Non-goals

- It will **not** fabricate experimental data, orders, patents or awards — by design.
- It will **not** predict whether you win or promise investment.
- It is **not** a generic engineering skill: no business/paper goal, no need for this skill.
- It does **not** replace real field experiments; every `【待填】` needs real data.

## License

MIT — see [LICENSE](LICENSE). Standards quoted in the references (GB/T 7714—2015 etc.) remain the property of their publishers; this repository only quotes formats and links.

## Acknowledgements

- Agent Skills specification — https://agentskills.io/specification
- anthropics/skills — https://github.com/anthropics/skills
- sevonsss/sevonsss-plan — https://github.com/sevonsss/sevonsss-plan
- xwu43361-sys/innovation-proposal — https://github.com/xwu43361-sys/innovation-proposal
- fengmo11/awesome-paper-research-skills — https://github.com/fengmo11/awesome-paper-research-skills
- O0000-code/awesome-academic-skills — https://github.com/O0000-code/awesome-academic-skills
- ustctug/ustcthesis — https://github.com/ustctug/ustcthesis
- 全国标准信息公共服务平台 — https://std.samr.gov.cn/


---

## 作者 / Author

**湖南科技大学 · 26 级 · 王越豪** · GitHub [@RazorEdge-wyh](https://github.com/RazorEdge-wyh)
