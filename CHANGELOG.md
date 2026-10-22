# Changelog

All notable changes to this project. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [Semantic Versioning](https://semver.org/).

## [1.2.0] — 2026-10-22

Open-source release.

### Added
- Agent Skills compliant frontmatter (`license`, `compatibility`, `metadata`) and install instructions
  for DSH / Claude Code / ZCode (`SKILL.md` §12, `docs/install.md`).
- `assets/templates/judging-mapping.md` — "scoring point ↔ section ↔ evidence" table, now a required
  BP deliverable.
- De-AI writing discipline (`SKILL.md` §3, `docs/writing-style.md`) and number tri-classification
  `[实测]/[估算]/[待补]`.
- `check_submission.py` v1.2: annotation-leak detection, label-style detection, evidence-marker
  statistics, judging-mapping check, `--mapping` skeleton generator, `--version`.
- `tools/validate_skill.py` — Agent Skills spec validator (stdlib fallback when PyYAML missing).
- `tools/install.ps1`, `tools/md2docx.py` (A4 / Chinese fonts / three-line tables / page footer).
- `tests/` — 17 unittest cases + fixtures; `.github/workflows/ci.yml` on Python 3.10/3.12/3.13.
- `docs/design.md`, `docs/format-comparison.md`, `docs/install.md`, `docs/writing-style.md`.
- Bilingual README (English / 中文), LICENSE (MIT), CONTRIBUTING, examples.

### Changed
- `SKILL.md` restructured: routing → iron rules → writing discipline → three workflows → quality gate
  → export → maintenance; references kept lazy-loaded.
- Citation checker now counts in-text citations only before the reference list (fixes false "ghost ref"
  results caused by counting reference entries themselves).
- Repo layout moved to `skills/jinzhongzi-cup/` (standard `<root>/<name>/SKILL.md`).

## [1.1.0] — 2026-10-22

### Added
- `references/08-paper-standards-verified.md` — 20 verified sources (GB/T 7714—2015, GB 7713—87,
  GB 6447—86, GB/T 15835, GB/T 15834, GB 3100, CY/T 174—2019, 教育部令第 40 号, AIGC 使用边界指南,
  NY/T 1536—2025, journal author guidelines…), each rule tagged `[核实 Sx]`.
- `references/09-contest-methodology.md` — 21 sources: three-edition weight evolution, 12-minute final
  (pitch 6 + Q&A 6), competition comparison (创新大赛 / 挑战杯 / 揭榜挂帅), 10 high-score patterns,
  14 disqualifying mistakes, fund due-diligence "three gates".

### Fixed
- Standard citation format (standard name first, standard number after colon).
- Page numbers for repeated citations placed outside the brackets (`[2]260`).
- Abstract must be third person, single paragraph, no figures/citations.
- Replicate count justified by error degrees of freedom (`df_e ≥ 12`) rather than "3 replicates";
  PLSD recommended over SSR/Duncan.
- AIGC disclosure five elements; academic-misconduct definitions (教育部令第 40 号, 学位法, CY/T 174).

## [1.0.0] — 2026-10-22

### Added
- Initial skill: competition rules baseline, project fact ledger, BP/pitch/paper workflows,
  AI-review adaptation, source grading (A>B>C>D), templates, and `check_submission.py` v1.0.
