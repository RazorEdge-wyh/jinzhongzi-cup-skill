#!/usr/bin/env python3
"""Validate Agent Skills bundles against the Agent Skills spec.

Checks each skill directory under a root:
  - <root>/<name>/SKILL.md exists
  - YAML frontmatter parses and contains required `name` (kebab-case, <=64, matches dir)
    and `description` (1..1024 chars)
  - optional `license` / `compatibility` are short strings; `metadata` is a string map
  - body is non-empty
  - relative resources mentioned in backticks (`references/...`, `assets/...`, `scripts/...`)
    actually exist

Usage:
  python validate_skill.py <root> [--json]
Exit codes: 0 = all valid, 1 = at least one problem.

Requires PyYAML (or, with no PyYAML, falls back to a minimal frontmatter parser).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

__version__ = "1.2.0"

KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESOURCE_REF = re.compile(r"`((?:references|assets|scripts)/[^`\s]+)`")
MAX_DESC = 1024
MAX_NAME = 64
MAX_COMPAT = 500


def parse_frontmatter(raw: str):
    """Return (data, body) or (None, None)."""
    if not raw.startswith("---\n"):
        return None, None
    end = raw.find("\n---", 3)
    if end < 0:
        return None, None
    fm = raw[4:end]
    body_start = raw.find("\n", end + 1)
    body = raw[body_start + 1 :] if body_start >= 0 else ""
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(fm)
        return (data if isinstance(data, dict) else None), body
    except Exception:
        # minimal fallback: key: value lines only
        data = {}
        for line in fm.splitlines():
            m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
            if m:
                data[m.group(1)] = m.group(2).strip().strip('"').strip("'")
        return (data or None), body


def validate_one(skill_md: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    raw = skill_md.read_text(encoding="utf-8", errors="replace")
    data, body = parse_frontmatter(raw)
    if not data:
        return ["缺少合法 YAML frontmatter（首行必须是 ---，且有闭合 ---）"], warnings

    name = data.get("name")
    desc = data.get("description")
    if not isinstance(name, str) or not name:
        errors.append("缺少必填字段 name")
    else:
        if len(name) > MAX_NAME:
            errors.append(f"name 超过 {MAX_NAME} 字符：{len(name)}")
        if not KEBAB.match(name):
            errors.append(f"name 不是 kebab-case：{name!r}")
        if name != skill_md.parent.name:
            errors.append(f"name({name}) 必须与目录名({skill_md.parent.name})一致")
    if not isinstance(desc, str) or not desc.strip():
        errors.append("缺少必填字段 description")
    elif len(desc) > MAX_DESC:
        errors.append(f"description 超过 {MAX_DESC} 字符：{len(desc)}")

    lic = data.get("license")
    if lic is not None and (not isinstance(lic, str) or not lic.strip() or len(lic) > 200):
        warnings.append("license 应为较短的许可名称/文件引用")
    compat = data.get("compatibility")
    if compat is not None and (not isinstance(compat, str) or len(compat) > MAX_COMPAT):
        errors.append(f"compatibility 必须是 1..{MAX_COMPAT} 字符的字符串")
    meta = data.get("metadata")
    if meta is not None:
        if not isinstance(meta, dict) or not all(isinstance(v, str) for v in meta.values()):
            errors.append("metadata 必须是 string→string 的映射")

    if not body.strip():
        errors.append("正文为空")

    for m in RESOURCE_REF.finditer(body):
        target = skill_md.parent / m.group(1)
        if not target.exists():
            errors.append(f"正文引用的资源不存在：{m.group(1)}")
    return errors, warnings


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Validate Agent Skills bundles")
    ap.add_argument("root", type=Path)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--version", action="version", version=f"validate_skill.py {__version__}")
    args = ap.parse_args()

    if not args.root.is_dir():
        raise SystemExit(f"目录不存在：{args.root}")

    results = []
    for entry in sorted(args.root.iterdir()):
        if not entry.is_dir():
            continue
        skill_md = entry / "SKILL.md"
        if not skill_md.is_file():
            results.append({"skill": entry.name, "ok": False, "errors": ["缺少 SKILL.md"], "warnings": []})
            continue
        errors, warnings = validate_one(skill_md)
        results.append({"skill": entry.name, "ok": not errors, "errors": errors, "warnings": warnings})

    if args.json:
        print(json.dumps({"version": __version__, "root": str(args.root), "results": results}, ensure_ascii=False, indent=2))
    else:
        for r in results:
            mark = "✓" if r["ok"] else "✗"
            print(f"{mark} {r['skill']}")
            for e in r["errors"]:
                print(f"   - {e}")
            for w in r["warnings"]:
                print(f"   ~ {w}")
        failed = sum(1 for r in results if not r["ok"])
        print(f"\n共 {len(results)} 个 skill，{failed} 个有问题")

    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
