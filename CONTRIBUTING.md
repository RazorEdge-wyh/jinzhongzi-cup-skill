# Contributing

Thanks for considering a contribution. This repository is a small, single-skill project; the goal is to keep it accurate, checkable and portable.

## Ways to contribute

| Type | What to do |
|---|---|
| Rule update | A new edition of the competition was announced → update `references/01-competition-rules.md` + `references/07-sources.md`, bump `metadata.version`, add a CHANGELOG entry |
| New competition | Add a section to `references/09-contest-methodology.md` (weight table + source links) and a row to the routing table in `SKILL.md` |
| Project swap | Replace `references/02-project-logic.md` with your project's fact ledger; keep the section structure |
| New check | Add a `check_*` function in `check_submission.py`, a fixture under `tests/fixtures/`, and a test case |
| Format/docs | Improve `docs/`, README, templates, or writing style guide |
| Bug | Open an issue with the input file (redacted), command and actual/expected output |

## Ground rules

1. **No fabricated facts.** Every number in the skill must have a source or be marked `[待补]`. PRs that add plausible-but-unsourced figures will be rejected.
2. **Cite sources.** Rules and standards need a link (official site preferred) and a verification date.
3. **Don't widen scope silently.** This skill targets Chinese college innovation & entrepreneurship competitions. Generic essay-writing features belong in another skill.
4. **Keep it portable.** Skill content must stay plain Markdown + stdlib Python. Optional dependencies must be documented.
5. **Chinese-first, English-available.** Primary content is zh-CN; README and docs keep an English counterpart where practical.

## Development

```bash
# tests
python -m unittest discover -s tests -v

# spec validation
python tools/validate_skill.py skills

# linter smoke tests
python skills/jinzhongzi-cup/scripts/check_submission.py tests/fixtures/plan_good.md --kind plan   # exit 0
python skills/jinzhongzi-cup/scripts/check_submission.py tests/fixtures/plan_bad.md --kind plan    # exit 1
```

Requirements: Python 3.9+; `pyyaml` and `python-docx` are optional (nice-to-have for full validation and
`.docx` reading).

## Commit / PR checklist

- [ ] `python -m unittest discover -s tests -v` passes
- [ ] `python tools/validate_skill.py skills` passes
- [ ] New rules have a source + verification date
- [ ] `CHANGELOG.md` updated (for user-visible changes)
- [ ] `SKILL.md` `metadata.version` bumped
- [ ] No secrets, tokens, personal WeChat/chat screenshots, or private project data committed
- [ ] Markdown renders correctly (tables, code fences)

## Reporting security / privacy issues

This repo contains no credentials and must never contain any. If you spot a leaked token, an accidental
screenshot with personal data, or a prompt-injection payload embedded in a doc, open an issue titled
`security:` (do not paste the sensitive content), or contact the maintainer via GitHub.
