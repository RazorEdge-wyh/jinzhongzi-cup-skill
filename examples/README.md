# 示例（Examples）

> 这里的文件是**教学示例**，用于展示"该写成什么样"，其中的数字与项目细节均为虚构，不可直接用于参赛。
> 真实材料请从 `skills/jinzhongzi-cup/assets/templates/` 开始填。

| 文件 | 展示什么 |
|---|---|
| `bp-before-after.md` | 同一段 BP 的"AI 味版本"与"去 AI 感版本"逐句对比 |
| `lint-report-sample.md` | linter 在一份问题材料上的真实输出（含如何逐条修） |

## 快速体验 linter

```bash
# 合规样例：退出码 0
python skills/jinzhongzi-cup/scripts/check_submission.py tests/fixtures/plan_good.md --kind plan

# 问题样例：退出码 1（缺章节、空话、批注残留、标签体）
python skills/jinzhongzi-cup/scripts/check_submission.py tests/fixtures/plan_bad.md --kind plan

# 生成"评审维度对照表"骨架
python skills/jinzhongzi-cup/scripts/check_submission.py --mapping
```
