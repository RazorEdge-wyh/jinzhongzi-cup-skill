# jinzhongzi-cup-skill

**面向中国大学生创新创业赛事的 agent skill：证据优先、格式正确、可机械校验。**

[English](README.md) · [设计说明](docs/design.md) · [格式对标](docs/format-comparison.md) · [安装](docs/install.md)

[![CI](https://github.com/RazorEdge-wyh/jinzhongzi-cup-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/RazorEdge-wyh/jinzhongzi-cup-skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v1.2.0-blue.svg)](CHANGELOG.md)

---

## 为什么做它

准备"金种子杯"、中国国际大学生创新大赛、挑战杯这类比赛时，材料写作有三类反复出现的问题：

1. **规则会漂移**：分值与权重逐届变化（市场 30→20、财务 15→20、社会价值 10→15），网上大量攻略已经过时。
2. **数据容易被编出来**：由 agent 生成的材料，最容易"顺手写一个看起来合理的数"，而这类比赛对真实性是一票否决。
3. **格式容易散**：BP、路演、论文三套材料各写各的，口径互相打架；GB/T 7714 引用细节多，人工核对成本高。

这个 skill 把这三件事变成**可执行的约束 + 一个能跑的 linter**，而不是一堆资料。

## 它提供什么

| 能力 | 具体做什么 |
|---|---|
| **权威赛制基线** | 第三届评分（25/20/20/20/15）、网评专家+AI 7:3、±15% 偏差复核、决赛 12 分钟（路演 6+答辩 6）、资格/材料/奖项/基金尽调 |
| **事实台账** | 每个断言先登记；数字分 `[实测]/[估算]/[待补]` 三类，再进正文 |
| **评审维度对照表** | "评分要点 ↔ 章节 ↔ 证据"三列表，BP 必交付物 |
| **去 AI 感写作纪律** | 叙述体优先、禁标签体、正文零批注、套话克制 |
| **论文工作流** | IMRaD、GB/T 7714—2015 著录模板、三线表、显著性字母标、AI 使用声明 |
| **提交前 linter** | 章节完整性、空话、无来源数字、批注残留、标签体、引用一致性、图表编号、五维覆盖 |
| **Word 导出** | `tools/md2docx.py` 输出 A4/宋体/黑体标题/三线表/页脚页码，再转 PDF |

## 快速开始

```bash
git clone https://github.com/RazorEdge-wyh/jinzhongzi-cup-skill.git
cd jinzhongzi-cup-skill
```

**DSH**（装到当前项目的 `.dsh/skills`）：

```powershell
.\tools\install.ps1 -Target dsh
```

**Claude Code / 通用 Agent Skills**：

```powershell
.\tools\install.ps1 -Target claude   # ~/.claude/skills
.\tools\install.ps1 -Target agents   # ~/.agents/skills
```

手动安装：把 `skills/jinzhongzi-cup/` 复制到运行时的技能目录，目录名必须保持 `jinzhongzi-cup`。

新开会话后：

```
/jinzhongzi-cup
用 jinzhongzi-cup 把方案扩成 BP
帮我检查这份 BP 能不能过网评
把试验写成 GB/T 7714 格式的论文
```

## 工作原理

```
SKILL.md                      路由 + 铁律 + 质量门
├── references/01 … 09        按需加载：赛制、项目事实、BP/路演、论文、统计、AI 评审、来源
├── assets/templates/         6 个填空模板（BP 骨架、答辩题库、论文大纲、
│                             试验方案、证据台账、评审维度对照表）
└── scripts/check_submission.py   提交前 linter
```

1. **渐进式加载**：`SKILL.md` 保持精简，细节用到才读。
2. **先证据后文字**：断言先登记、后写作。
3. **机械检查**：交稿前跑 linter；缺章节、引用断裂会直接失败。
4. **格式可追溯**：每个格式选择的依据都写在 [docs/format-comparison.md](docs/format-comparison.md)。

## 仓库结构

```text
jinzhongzi-cup-skill/
├── skills/jinzhongzi-cup/     # skill 本体（遵循 Agent Skills 规范）
│   ├── SKILL.md
│   ├── references/            # 9 个参考文档
│   ├── assets/templates/      # 6 个模板
│   └── scripts/check_submission.py
├── tools/                     # md2docx.py、validate_skill.py、install.ps1
├── tests/                     # 17 个单元测试 + fixtures
├── docs/                      # 设计、格式对标、安装、写作风格
├── examples/                  # 示例产出（明确标注为示例）
├── .github/workflows/ci.yml   # 测试 + 规范校验 + linter fixtures
├── CHANGELOG.md · CONTRIBUTING.md · LICENSE
└── README.md / README.zh-CN.md
```

## 校验

```bash
python -m unittest discover -s tests -v      # 17 tests
python tools/validate_skill.py skills        # Agent Skills 规范校验
python skills/jinzhongzi-cup/scripts/check_submission.py --version
python skills/jinzhongzi-cup/scripts/check_submission.py --mapping
python skills/jinzhongzi-cup/scripts/check_submission.py tests/fixtures/plan_bad.md --kind plan  # 退出码 1
```

CI 在 Python 3.10 / 3.12 / 3.13 上跑同一套命令。

## 与现成项目的对比

| 项目 | 定位 | 本 skill 的差异 |
|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | 官方技能示例 | 遵循同一规范与布局，但提供**赛事专用**工作流 + linter + 测试 |
| [sevonsss/sevonsss-plan](https://github.com/sevonsss/sevonsss-plan) | 中文 BP skill，60–80 页十章 | 采纳其**去 AI 感六条**与数字三分类；但本项目只做 25–35 页，因为这里评分看"结构与证据"而非篇幅 |
| [xwu43361-sys/innovation-proposal](https://github.com/xwu43361-sys/innovation-proposal) | 内嵌官方评分表的申报书 skill | 采纳其**评审维度对照表**，并补上可运行的 linter 与测试 |
| [fengmo11/awesome-paper-research-skills](https://github.com/fengmo11/awesome-paper-research-skills) | 论文技能索引 | 我们是单个可安装 skill；仓库格式（双语 README、徽章、CI、CHANGELOG）向这个生态看齐 |
| [ustctug/ustcthesis](https://github.com/ustctug/ustcthesis) | LaTeX 学位论文模板 | 不提供 LaTeX 模板，改为"GB/T 7714 规则 + 检查清单"，覆盖 Word 投稿/毕设场景 |

逐项"采纳/放弃"的理由见 [docs/format-comparison.md](docs/format-comparison.md)。

## 不做什么

- 不生成、不美化实验数据/订单/专利/获奖（设计原则）。
- 不预测获奖、不承诺投资。
- 不做纯工程设计；没有商业/论文目标时不需要本 skill。
- 不替代真实田间实验：所有 `【待填】` 都要真实数据。

## 许可证

MIT，见 [LICENSE](LICENSE)。参考文档中引用的国标（GB/T 7714—2015 等）版权归发布机构，本仓库只引用格式与链接，不分发标准原文。

## 致谢

- Agent Skills 规范 — https://agentskills.io/specification
- anthropics/skills — https://github.com/anthropics/skills
- sevonsss/sevonsss-plan — https://github.com/sevonsss/sevonsss-plan
- xwu43361-sys/innovation-proposal — https://github.com/xwu43361-sys/innovation-proposal
- fengmo11/awesome-paper-research-skills — https://github.com/fengmo11/awesome-paper-research-skills
- O0000-code/awesome-academic-skills — https://github.com/O0000-code/awesome-academic-skills
- ustctug/ustcthesis — https://github.com/ustctug/ustcthesis
- 全国标准信息公共服务平台 — https://std.samr.gov.cn/
