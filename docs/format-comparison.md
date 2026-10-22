# 格式对标与借鉴说明（Format Comparison）

> 本文件回答一个问题：**这个 skill 的格式不是拍脑袋定的，而是对着哪些现成标准/项目做的、采纳了什么、放弃了什么。**
> 对比时间：2026-10-22。所有外部项目均给出可访问链接；引用只作格式参考，不复制其内容。

## 1. 对比对象一览

| 类别 | 对象 | 链接 | 我们借鉴的点 |
|---|---|---|---|
| Agent Skill 规范 | Agent Skills Specification | https://agentskills.io/specification | `SKILL.md` frontmatter 字段（name/description/license/compatibility/metadata）、`scripts/ references/ assets/` 目录约定、渐进式加载 |
| 官方技能库 | anthropics/skills | https://github.com/anthropics/skills | 仓库布局（`skills/<name>/`、`spec/`、`template/`）、每个 skill 自带 LICENSE、README 的安装/试用/免责声明结构 |
| 论文技能索引 | fengmo11/awesome-paper-research-skills | https://github.com/fengmo11/awesome-paper-research-skills | 双语 README、版本徽章、"Why This Exists"、按研究生命周期分节、CI 校验、CHANGELOG |
| 学术技能索引 | O0000-code/awesome-academic-skills | https://github.com/O0000-code/awesome-academic-skills | 条目注明许可证与运行方式、按科研阶段组织 |
| 中文 BP 技能 | sevonsss/sevonsss-plan | https://github.com/sevonsss/sevonsss-plan | **去 AI 感写作纪律**（禁标签体/禁正文批注/套话克制）、数字三分类、`references/` 路由表、Word 排版规范 |
| 中文申报书技能 | xwu43361-sys/innovation-proposal | https://github.com/xwu43361-sys/innovation-proposal | **评审维度对照表**、待补信息清单、file map、五步工作流、"评分表驱动写作" |
| 学位论文格式 | ustctug/ustcthesis | https://github.com/ustctug/ustcthesis | 学位论文的结构层次、图题表题、参考文献实现方式（作为"交付格式"参考，不直接复用 LaTeX） |
| 引用国标 | GB/T 7714—2015 | https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D8055ED3A7E05397BE0A0AB82A | 顺序编码制、9 类文献著录格式（见 `references/08`） |
| 编写格式国标 | GB 7713—87 | 见 `references/08` 来源表 S3 | 摘要/关键词/图表/章节编号 |
| 数字与单位国标 | GB/T 15835、GB 3100~3102、GB/T 15834 | https://openstd.samr.gov.cn/ | 数字用法、量与单位、标点 |

## 2. 逐项采纳/放弃

| 维度 | 现成做法 | 我们的做法 | 为什么 |
|---|---|---|---|
| SKILL.md 元数据 | name + description（+ license/metadata） | 全字段，含 `license`、`compatibility`、`metadata`（版本/赛事/标准） | 兼容 Agent Skills 规范，同时让 skill 可被审计 |
| 目录结构 | `scripts/ references/ assets/` | 完全遵循；`05/06/07` 为按需加载的 reference | 渐进式加载，避免上下文塞满 |
| BP 篇幅 | 中文 BP 技能常见 60–80 页十章 | **25–35 页 12 节** | 金种子杯网评是"3–8 分钟速读 + AI 抽取"，长文档反而丢分；长版可参考 sevonsss-plan |
| 写作纪律 | sevonsss-plan 的"去 AI 感"六条 | 采纳并压缩为 6 条，新增"正文零批注"与"提交前跑 linter" | 评委能感知 AI 味；我们的材料默认由 agent 生成，必须显式约束 |
| 数字标注 | 三分类 `[真实数据]/[估算假设]/[待补充]` | 改为 `[实测]/[估算]/[待补]`，并接入证据台账与 linter | 更短、适合中文正文；能被脚本机械检查 |
| 评分对齐 | innovation-proposal 的"评审维度对照表" | 采纳为**必交付物**，新增 `assets/templates/judging-mapping.md` 与 linter 检查 | 直接解决"每章回应哪条评分"的问题 |
| 论文格式 | 学位论文 LaTeX 模板 | 不提供 LaTeX 模板，改为"格式规则 + 检查清单 + GB/T 7714 实例" | 用户多投期刊/毕设，Word 更通用；LaTeX 用户可直接套 ustcthesis |
| 引用校验 | 人工核对 | `check_submission.py` 机械校验正文 `[n]` ↔ 文末列表 | 幽灵引用/缺失引用是常见扣分点 |
| 仓库形态 | awesome 索引型 / 单 skill 型 | 单 skill + tools + tests + docs + CI | 可直接安装使用，也可作为"带校验的 skill"参考模板 |
| README | 双语 + 徽章 + Why + 安装 + 免责声明 | 采纳（英/中双语，CI/许可/版本徽章，安装三种运行时） | 开源项目第一眼可信度 |
| 许可证 | anthropics/skills 多为 Apache-2.0；索引库 CC0 | **MIT**（代码与文档），文档中引用的国标/官方文件不重新授权 | 最宽松、便于二次使用；国标文本不在本仓库分发 |

## 3. 我们**没有**照搬的东西（及原因）

1. **60–80 页十章 BP 结构**：那是国赛/商业计划书比赛的体量；金种子杯网评 + 12 分钟决赛更看"结构与证据"，长文反而稀释。
2. **按赛事内置全部评分表**：我们只内置金种子杯第三届 + 横向对照表；其它赛事建议用户提供当届评分表（避免规则过期误导）。
3. **LaTeX 模板**：维护成本高、与 Word 交付冲突；只给格式规则与引用实例。
4. **"教育维度/育人叙事"**：金种子杯不设该维度，创新大赛才重；放在 `09` 的对照表里提示，不写进主流程。
5. **花哨的自动化流水线**（pipeline/JSON 编排）：本 skill 定位"单文件可读 + 一个 linter"，不引入运行时依赖。

## 4. 格式合规自检

- [x] `SKILL.md` frontmatter 通过 `tools/validate_skill.py`（name/description/license/compatibility/metadata）
- [x] 目录含 `references/ assets/ scripts/`，资源引用全部存在
- [x] README 双语、含安装/使用/对比/许可/致谢
- [x] 有 `LICENSE`、`CHANGELOG.md`、`CONTRIBUTING.md`、CI
- [x] 论文格式遵循 GB/T 7714—2015 与 GB 7713—87（见 `references/04`、`08`）
- [x] 文档内的外部链接均可访问（2026-10-22 核对）

## 5. 参考项目链接汇总

- https://agentskills.io/specification
- https://github.com/anthropics/skills
- https://github.com/fengmo11/awesome-paper-research-skills
- https://github.com/O0000-code/awesome-academic-skills
- https://github.com/sevonsss/sevonsss-plan
- https://github.com/xwu43361-sys/innovation-proposal
- https://github.com/ustctug/ustcthesis
- https://std.samr.gov.cn/ （国家标准全文公开系统）
- https://openstd.samr.gov.cn/ （标准信息公共服务平台）
