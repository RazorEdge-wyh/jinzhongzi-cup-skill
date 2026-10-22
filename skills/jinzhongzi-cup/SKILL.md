---
name: jinzhongzi-cup
description: >-
  Evidence-led agent skill for Chinese college innovation & entrepreneurship competitions
  (金种子杯 / 中国国际大学生创新大赛 / 挑战杯): turn a raw project idea into a defensible
  business plan, a 6-minute pitch with Q&A, and a GB/T 7714 paper draft. Ships verified
  competition rules (three-edition score-weight evolution, expert+AI 7:3 network review,
  12-minute final), a project fact ledger with source grading, judging-dimension mapping,
  a submission linter, and Word/PDF export. Use when writing or reviewing
  商业计划书/BP/项目书/路演/答辩稿/论文/研究报告/试验方案, or when checking competition
  rules, scoring criteria and material compliance.
license: MIT
compatibility: >-
  Agent Skills compatible runtime (DSH, Claude Code, ZCode, etc.). Optional scripts need
  Python 3.9+ and stdlib only; DOCX/PDF export additionally needs python-docx and
  LibreOffice (bundled in DSH).
metadata:
  author: RazorEdge-wyh
  version: "1.2.0"
  updated: "2026-10-22"
  languages: "zh-CN, en"
  competition: '第三届“金种子杯”大学生创业大赛（湖南省人民政府主办）'
  domain: "microbial agriculture / smart agriculture"
  standards: "GB/T 7714—2015, GB 7713—87, GB/T 15835, GB 3100, GB/T 15834"
---

# 金种子杯：项目 · 比赛 · 论文 工作流

> 这是一个**可执行的工作流**，不是资料集。先按 §1 路由，再动手；每份产出都要过 §7 质量门。
> 默认场景：湖南"金种子杯"现代农业与大健康产业赛道；其它赛事按 `references/09-contest-methodology.md` 的对照表切换权重。

## 0. 适用与不适用

**适用**：写/改项目书与商业计划书（BP）；做 6 分钟路演与答辩；写论文/研究报告/试验方案；核对赛事规则与评分口径；材料提交前自检；把材料导出 Word/PDF。

**不适用**（这时应当拒绝或转交）：
- 要求代写、伪造或"美化"实验数据/订单/专利/获奖 → 直接拒绝，改为列"待补证据清单"。
- 要求预测获奖结果、承诺投资 → 只给材料层面的改进建议。
- 纯工程设计（不带商业/论文目标）→ 不需要本 skill。
- 需要真实实验数据而用户没有 → 只能产出带 `[待补]` 标记的方案与空白表。

## 1. 先路由：这次要做的是什么

| 用户意图 | 先读 | 用模板 | 产出 |
|---|---|---|---|
| 写/改项目书、商业计划书（BP） | `references/02-project-logic.md` → `references/03-plan-and-deck.md` | `assets/templates/project-plan-skeleton.md` | 结构化 Markdown + **评审维度对照表** |
| 做路演 PPT / 讲稿 / 答辩 Q&A | `references/03-plan-and-deck.md` | `assets/templates/defense-qa-bank.md` | 页级大纲 + 逐页口播稿 + 15 问答案 |
| 写论文 / 研究报告 / 试验方案 | `references/04-paper-writing.md` → `references/05-data-and-statistics.md` | `assets/templates/paper-outline.md`、`experiment-plan.md` | IMRaD 论文或研究报告 |
| 查赛道、时间、评分、奖项、资格 | `references/01-competition-rules.md` | — | 带来源与核实日期的规则摘要 |
| 材料要过 AI 初筛 / 自查可解析性 | `references/06-ai-review.md` | — | 结构化改写 + 量化指标补齐 |
| 需要知道某条规则/标准的出处 | `references/07-sources.md` | — | 可点击来源 + 核实状态 |
| 横向对照其它赛事 / 高分与扣分清单 | `references/09-contest-methodology.md`、`01` §7.5 | — | 规则对照表 + 方法论 |
| 需要核对某条国标条款 | `references/08-paper-standards-verified.md` | — | 20 个来源逐条 `[核实 Sx]` |

需要生成 `.docx` / `.pptx` / `.xlsx` 时，优先用所在运行时自带的文档技能（DSH 为 `office-docx` / `office-pptx` / `office-xlsx`），或本仓库 `tools/md2docx.py`（Markdown → Word，配合 LibreOffice 转 PDF）。

## 2. 三条铁律 + 数字三分类

1. **不编造证据**：任何数字必须来自本项目实验 / 公开文献 / 官方统计 / 用户资料。文献结论只支撑其原始条件，不做跨作物、跨区域外推。
2. **口径唯一**：活菌数（CFU/g 鲜土）、窗口期（0–30 天）、判定时点（第 7/15 天）、单点成本——全链路同名同单位；改一处必须全链路同步。
3. **以第三届为准**：分值权重一律用第三届（25/20/20/20/15）；第二届文件只作"评分内容措辞"参考，并注明届次。

**数字三分类（写作时强制标注，定稿前统一清理）**：

| 标记 | 含义 | 用法 |
|---|---|---|
| `[实测]` | 有实验/检测/合同/官方统计支撑 | 可进正文，附来源与 n |
| `[估算]` | 有推导但无直接数据 | 写清假设与区间，答辩时说"这是假设" |
| `[待补]` | 目前没有，必须补 | 写成"目标值/待验证"，并进证据台账 |

所有断言先进 `assets/templates/evidence-ledger.md` 登记，再写进材料；`[实测]` 不足的材料不得进入正式提交版。

## 3. 去 AI 感写作纪律（评审可感知）

AI 生成文本的典型败笔是"标签体 + 表格轰炸 + 文内批注 + 华丽套话"，一眼就会被评委识破。写作时强制自查：

1. **叙述体优先，禁标签体**：正文用连贯段落，禁止"定位宣言：""核心逻辑：""一句话概括：""系统架构一句话："这类"标签+冒号"句式，禁止用反引号代码块拼卖点。
2. **段落为主、表格为辅**：表格只用于参数/财务/竞品对比/画布等必须对齐的内容，且每张表前有过渡句（"具体参数见下表"）。
3. **正文零批注**：`[实测]/[估算]/[待补]`、`[核实 Sx]`、"> 自检清单"、emoji、⚠️/✅/★ 都是写作过程标记，**提交版必须清掉**；数据诚实性由"文首数据声明 + 财务基本假设"承担。
4. **套话克制**："硬件为入口、订阅为粘性"这类对仗金句全篇最多一处；禁止每章重复"闭环/赋能/双轮驱动/数据飞轮"。
5. **图表规范**：图题在图下、表题在表上；图号按章编排（图 1-1）；正文用"如图 X 所示"引导。
6. **语气**：像认真参赛的学生团队在陈述——具体、有细节（型号/数量/场景/用户原声），少用营销腔与空形容词。

> 提交前跑 `scripts/check_submission.py`：它会检查空话、无来源数字、正文批注残留、标签体、引用一致性。

## 4. 工作流 A：项目书 / BP

目标：让评委 3 分钟看懂"真需求—真方案—真证据—真能落地"，按五维组织而不是按论文逻辑组织。

1. **定赛道与组别**：本项目报"现代农业与大健康产业"；确认在校生/毕业 5 年内、是否已注册企业（决定材料清单）。
2. **写一句话价值主张**：`为<谁>在<什么时刻>解决<什么损失>，用<什么手段>，成本<多少>`。先取 `02-project-logic.md` §1 的现成版本。
3. **搭证据链**：痛点 → 事实 1/2/3 → 缺口（现有方案为何不覆盖）→ 本方案 → 可测指标。每个"事实"必须能追到引文，并登记进证据台账。
4. **对齐五维**（`01` §7.3）：产品创新 25 / 产业认知与市场 20 / 团队 20 / 财务 20 / 社会价值 15。每维一个一级标题，标题直接回应评分要点。
5. **补商业侧**：客户与渠道、定价与单位经济模型（单点 150 元 → 亩均 → 每亩增收）、财务三表假设、里程碑与资金用途、在湘落地计划。
6. **交"评审维度对照表"**：用 `assets/templates/judging-mapping.md`，把"评分要点 ↔ 章节 ↔ 证据"三列填满；填不满的地方就是缺证据。
7. **跑质量门**：`check_submission.py --kind plan` + §7 自检表 + 去 AI 感自查。

## 5. 工作流 B：路演与答辩

1. **评分结构**：决赛专家 + 大众 7:3；大众四项＝落地可信度 30 / 产业匹配度 30 / 社会贡献度 30 / 持续成长 10（`01` §7.4）。
2. **时间**：决赛 12 分钟 = **路演 6 + 答辩 6**（第三届口径）。6 分钟分镜：一句话+田间图 30s → 痛点与证据 90s → 方案与三个不同点 90s → 已验证进展 60s → 落地与财务 50s → 团队+收尾 40s。
3. **每页一个论点**，标题写结论不写名词；数字上大字号，来源放页脚。
4. **答辩公式**：结论 → 证据 → 边界/风险 → 下一步验证。禁止"我们觉得/应该会/市场很大"。
5. **15 问清单**见 `03-plan-and-deck.md` §6.6（菌株保藏、检测方法、补施对比、传感器漂移、BOM、付费意愿、极端天气、与厂商关系、IP 归属、数据核查、毛利、服务半径、回购、全职比例、失败预案）。

## 6. 工作流 C：论文 / 研究报告

1. 判定体裁：研究报告（给评委/投资看）还是学术论文（投稿/毕设）。
2. IMRaD：引言（问题与缺口）→ 材料与方法（可复现）→ 结果（只陈述）→ 讨论（解释、边界）→ 结论。
3. 方法必写清：试验地/品种/菌株/剂量/对照（含"只补墒不接菌"组）/重复数（df_e≥12）/随机化/测定时点/活菌数测定/统计方法。
4. 图表：三线表、图题在下表题在上、单位、误差棒类型、显著性标注、n。
5. 引用：GB/T 7714—2015 顺序编码制（`04` §4 操作模板；`08` 国标出处）。
6. **留白纪律**：需真实环境验证的数据一律写 `【待填：指标 + 时点 + 方法】`，不写"预计将达到"充数。

## 7. 质量门（提交前逐项打勾）

项目书/BP：
- [ ] 一句话价值主张 20 秒可读完（谁/何时/什么损失/什么手段/多少成本）
- [ ] 五维各有一级标题，且每个评分要点都有对应段落
- [ ] 关键数字有来源；`[实测]/[估算]/[待补]` 三类比例合理，无"估算冒充实测"
- [ ] 有"现有方案为何不够"的对比
- [ ] 单位经济模型可复算（单点成本、覆盖面积、亩均投入与收益）
- [ ] 有对照设计与判定指标（第 7/15 天根际活菌数）
- [ ] 有风险表（技术/市场/政策/团队）与缓解动作
- [ ] 有在湘落地计划（园区/合作方/时间表）
- [ ] 无"国际领先/填补空白/颠覆"等无证据最高级表述
- [ ] 有评审维度对照表；`check_submission.py` 通过；正文无批注残留

路演：
- [ ] 6 分钟版与 3 分钟版都能讲完，不超时
- [ ] 每页标题是结论
- [ ] 三个不同点脱稿可讲，各配一条证据
- [ ] 15 个尖锐问题有"结论—证据—边界—下一步"答案
- [ ] 大众评审四维各有一句能被记住的话

论文：
- [ ] 方法可复现（他人照做能重做）
- [ ] 结果与讨论分开，结果节不出现因果解释
- [ ] 三线表/题注位置/单位/误差棒/显著性齐全
- [ ] 引用与文末一一对应，GB/T 7714—2015
- [ ] 明确外推边界（草莓结论不外推水稻/茶叶）
- [ ] AI 使用按目标单位要求声明

## 8. 输出与导出

- 中间稿 Markdown；成稿转 DOCX/PDF。命名：`<项目>-<材料类型>-v<主>.<次>-<日期>`。
- 导出：`python tools/md2docx.py <in.md> <out.docx>`（A4/宋体五号/黑体标题/三线表/页脚页码），再 `libreoffice-kit convert` 或 Word 导出 PDF。
- 每次交付附：`改了什么 / 依据哪条规则 / 还缺什么证据`（三行即可）。

## 9. 事实与来源政策

- 规则类：只写 `01` 里带来源的条目；未核实加 `[未核实]`；冲突时以组委会正式通知/报名系统为准。
- 文献类：作者 + 年份 + 刊名/学位授予单位；二手转述标"转引自"；AI 给出的题录必须逐条核原文。
- 用户口述：当作"待补证"，写"（待提供佐证）"。
- 不预测评审结果、不承诺获奖、不代替用户做真实性承诺。

## 10. 资源索引

- `references/01-competition-rules.md` — 第三届赛制基线（权重演变/12 分钟/大众评审/材料清单）
- `references/02-project-logic.md` — 项目卡：一句话、证据链 F1–F8、机制、BOM、口径、风险、缺口
- `references/03-plan-and-deck.md` — BP 12 节、单位经济模型、6 分钟分镜、答辩 20 题+15 问、扣分红线
- `references/04-paper-writing.md` — 论文速查（结构/摘要/图表/引用/中文规范/AI 声明）
- `references/05-data-and-statistics.md` — 试验设计、活菌数测定、统计决策树、数据表
- `references/06-ai-review.md` — 网评 AI（30%）适配：可解析性、AI 友好段落、空话黑名单
- `references/07-sources.md` — 来源总账 + 权威性分级 A>B>C>D
- `references/08-paper-standards-verified.md` — 论文规范权威核实版（20 来源，逐条溯源）
- `references/09-contest-methodology.md` — 赛事方法论权威核实版（21 来源、三赛对照、扣分红线）
- `assets/templates/` — BP 骨架、答辩题库、论文大纲、试验方案、证据台账、**评审维度对照表**
- `scripts/check_submission.py` — 提交前自检（结构/空话/来源/批注/标签体/引用/五维覆盖）

## 11. 三个典型请求的执行路径

1. **"把方案扩成金种子杯 BP"** → 读 `02` 取事实 → 填 `project-plan-skeleton` → 按 `01` §7.3 对齐 → 填 `judging-mapping` → 跑 `--kind plan` → 列缺口 → 需要 DOCX 时加载 `office-docx`。
2. **"下周路演，做 6 分钟 PPT 与答辩"** → 读 `03` §5 分镜 → 结论式标题 → 从 `02` 抽数据做 3 张核心图 → `03` §6.6 十五问 + `defense-qa-bank` 演练 → 用 `office-pptx` 出片。
3. **"把试验写成论文投期刊"** → 读 `04` 结构 + `05` 统计 → `experiment-plan` 锁方案 → 填 `paper-outline` → 核 GB/T 7714 → 跑 `--kind paper`。

## 12. 兼容与安装（Agent Skills）

本 skill 遵循 Agent Skills 规范（`SKILL.md` + `references/` + `assets/` + `scripts/`），可放到任意兼容运行时的技能目录：

| 运行时 | 安装位置 |
|---|---|
| DSH | `<project>/.dsh/skills/jinzhongzi-cup/` 或 `~/.dsh/skills/...` |
| Claude Code / 通用 | `~/.claude/skills/jinzhongzi-cup/` 或 `~/.agents/skills/...` |
| 项目内共享 | `<repo>/.agents/skills/jinzhongzi-cup/` |

也可用本仓库 `tools/install.ps1 -Target dsh|agents|claude` 一键复制。安装后新开会话即可用 `/jinzhongzi-cup` 或让助手自动加载。

## 13. 维护与版本

- 赛制变化：只改 `01` + `07` 的核实日期与来源；方法论/对照改 `09`。
- 项目新数据：只改 `02`，同步证据台账。
- 论文规范：先查 `08`（出处），再改 `04`（速查）。
- 每次改动跑 `tests/`（`python -m unittest discover -s tests`）与 `tools/validate_skill.py`。

**变更记录**：见仓库 `CHANGELOG.md`。
