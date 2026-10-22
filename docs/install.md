# 安装与验证（Install)

本 skill 遵循 [Agent Skills 规范](https://agentskills.io/specification)：一个目录 + `SKILL.md`，可选 `references/`、`assets/`、`scripts/`。任何兼容该规范的运行时都能加载。

## 1. 选择安装位置

| 运行时 | 位置 | 说明 |
|---|---|---|
| DSH（DeepSeek Harness） | `<项目>/.dsh/skills/jinzhongzi-cup/` | 项目级，随项目走；或 `~/.dsh/skills/` 用户级 |
| Claude Code | `~/.claude/skills/jinzhongzi-cup/` | 用户级；项目级可放 `<repo>/.claude/skills/` |
| ZCode / 其它（读取 `~/.agents/skills`） | `~/.agents/skills/jinzhongzi-cup/` | 多 runtime 共享 |
| 仓库内共享 | `<repo>/.agents/skills/jinzhongzi-cup/` | 团队统一版本 |

目录名必须与 `SKILL.md` 的 `name` 一致（`jinzhongzi-cup`），否则校验失败。

## 2. 安装方式

### 方式 A：一键脚本（Windows PowerShell）

```powershell
# 先克隆
git clone https://github.com/RazorEdge-wyh/jinzhongzi-cup-skill.git
cd jinzhongzi-cup-skill

# 装到当前目录的 .dsh/skills（默认）
.\tools\install.ps1

# 或指定运行时
.\tools\install.ps1 -Target agents     # ~/.agents/skills
.\tools\install.ps1 -Target claude     # ~/.claude/skills
.\tools\install.ps1 -Dest D:\my\skills # 任意目录
```

### 方式 B：手动复制

```bash
# Linux / macOS
mkdir -p ~/.agents/skills
cp -r skills/jinzhongzi-cup ~/.agents/skills/

# Windows PowerShell
New-Item -ItemType Directory -Force "$HOME\.agents\skills"
Copy-Item -Recurse .\skills\jinzhongzi-cup "$HOME\.agents\skills\"
```

### 方式 C：只取文件（不装 git）

从 GitHub 页面下载 ZIP → 解压 → 把 `skills/jinzhongzi-cup/` 放进对应技能目录。

## 3. 验证

```bash
# 1) 规范校验（frontmatter、目录名、资源引用）
python tools/validate_skill.py ~/.agents/skills

# 2) linter 自检
python ~/.agents/skills/jinzhongzi-cup/scripts/check_submission.py --version
python ~/.agents/skills/jinzhongzi-cup/scripts/check_submission.py --mapping

# 3) 运行时验证
# DSH：新开会话后输入 /jinzhongzi-cup，或让助手调用 skill(name="jinzhongzi-cup")
# Claude Code：/jinzhongzi-cup
```

## 4. 依赖

| 功能 | 依赖 |
|---|---|
| 核心（读/写/路由） | 无 |
| linter | Python 3.9+（仅标准库） |
| 读 `.docx` | python-docx |
| Markdown → Word | python-docx（`tools/md2docx.py`） |
| Word/PDF 转换 | LibreOffice（DSH 自带；其它环境装 LibreOffice 或 Word 导出 PDF） |

## 5. 卸载与升级

- 卸载：删除对应技能目录（`rm -rf ~/.agents/skills/jinzhongzi-cup`）。
- 升级：`git pull` 后重新运行 `install.ps1 -Force`；或直接覆盖目录。
- 版本：见 `CHANGELOG.md` 与 `SKILL.md` 的 `metadata.version`。

## 6. 常见问题

| 现象 | 原因 / 处理 |
|---|---|
| 技能列表里看不到 | 目录名与 `name` 不一致；或运行时未开启 skills 目录扫描（DSH 见仓库根 README 的"已知环境问题"） |
| `validate_skill.py` 报 name 不一致 | 安装时目录被改名，改回 `jinzhongzi-cup` |
| linter 报大量"数字无来源" | 正常：先把数字登记进证据台账，再在句子里带来源 |
| DOCX 转换失败 | 未装 python-docx / LibreOffice；或输出文件已存在（需换新文件名） |
