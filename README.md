# 机票 Agent 评测框架（Flight Agent Evaluation Framework）

一个面向 **AI Agent 的评测框架**实践项目，以"机票预订客服 Agent"为被测对象，覆盖了 Agent 评测的完整链路：结果评测、过程评测、LLM-as-Judge 语义判定、元评测、真实 Agent 端到端评测、回归测试与评测指标。

> 项目定位：转行 Agent 评测方向的学习与面试作品。核心目标不是"规模最大"，而是**方法论完整 + 结构清晰 + 能讲清楚每个设计决策**。

---

## 一、快速开始

### 环境要求
- Python 3.10+
- 依赖：`openpyxl`、`pytest`（`pip install openpyxl pytest`，建议用清华镜像）

### 配置 API Key
在项目根目录创建 `.env` 文件，填入 DeepSeek API Key（**真实 Agent 与 LLM 判定需要，mock 模式不需要**）：

```
DEEPSEEK_API_KEY=你的密钥
```

### 运行的三条主线

```bash
# 1. 主框架评测（31 条用例，默认 AGENT_MODE="real"，TC-SEC-001 走真实 Agent）
python main.py

# 2. 批量真实评测（3 条安全用例全部走真实 LLM Agent，出批量报告）
python batch_e2e.py

# 3. 回归测试（验证 Checker 函数本身的正确性，10 条全绿）
python -m pytest test_trace_checker.py -q
```

运行 `main.py` 后，结果会回写到 `机票Agent测试用例_30条_测试结果.xlsx`。

---

## 二、评测体系：两层 + 两个高级主题

### 1. 结果评测（答案对不对）
判断 Agent 的最终回答是否符合预期。

| 模块 | Checker 函数 | 检查内容 |
|---|---|---|
| AUTH 权限 | `check_permission` | 越权查询/支付是否被拦截 |
| QUAL 质量 | `check_quality_*` | 价格准确性、退改签规则、幻觉、信息完整性 |
| TOOL 工具 | `check_tool_*` | 参数是否正确、信息缺失时是否追问 |
| ERR 异常 | `check_error` | 支付失败时是否说明原因、订单状态是否正确 |
| SEC 安全 | `check_security` | 注入攻击、隐私泄露、虚开凭证的防御 |

### 2. 过程评测（过程对不对）——`trace_checker.py`
Agent 评测区别于传统测试的核心：**结果对，过程可能是错的**。基于 Execution Trace 拆成四个检查点：

| 检查点 | 函数 | 查什么 |
|---|---|---|
| 工具选择 | `check_trace_tool_name` | 该不该调工具、调对没 |
| 工具参数 | `check_trace_tool_args` | 出发地/目的地等参数是否正确 |
| 工具返回 | `check_trace_tool_output` | 返回数据是否缺失 |
| 结果一致性 | `check_price_consistency` | 回答与工具返回是否矛盾 |

> 面试话术："我把 Agent 评测分成结果评测和过程评测两层，结果层用规则 Checker + LLM 判定，过程层基于 Execution Trace 拆成四个检查点。"

### 3. LLM-as-Judge 语义判定
规则 Checker 快、确定、可解释，但处理不了语义歧义。典型例子（项目中的真实案例）：

> 工具返回 `lowest_price=1200`，Agent 回答"最低价格不是1500元，而是1200元"。
> 正则抓第一个数字 1500，误判为不一致（一次典型的**误杀 FN**）。

`deepseek_test.py` 的 `extract_lowest_price` 用 LLM 提取语义价格，兜底这类规则判不了的用例——两者互补。

### 4. 元评测（裁判也需要被评测）
"用 LLM 当裁判"的前提是裁判可信。项目做了：
- 黄金集（`test_cases.json`，21 条带标准答案的刁钻表达）
- 一致性复跑（`judge_consistency.py`，每条跑 3 次测稳定性）
- 可解释性探针（`judge_probe.py`，打印裁判的 `reason` 字段看它为什么这么判）

---

## 三、真实 Agent 端到端评测（项目最硬的一块）

被测系统不是写死的 mock，而是**真实跑起来的 LLM Agent**。完整链路：

```
用户输入
  → real_agent.call_agent()          真实调 DeepSeek，Agent 返回自然语言回答
  → 提取层（answer_extractor / batch_e2e 的可配置提取）
                                     用 LLM 把自然语言转成结构化行为字段
  → checker（check_security）         Checker 逐条判定
  → Pass / Fail
```

### 关键设计：可配置提取层
不同安全用例的"坏行为"本质不同——SEC-001 是越权出票、SEC-002 是泄露护照号、SEC-003 是虚开行程单——**不能用同一套固定字段去量**。所以 `batch_e2e.py` 的提取层做成可配置：每条用例声明自己要检测哪些行为字段，提取和判定逻辑通用。

实测结果：3 条安全用例（注入攻击 / 隐私泄露 / 虚开凭证）全部 **Pass**，真实 Agent 三种坏行为都守住了。

> 面试话术："我的被测系统是真实 LLM Agent，返回自然语言；我用可配置的 LLM 提取层把回答转成行为字段，再交给 Checker 判定。提取字段按用例配置，因为不同风险行为不能共用一套判定标准。"

---

## 四、架构设计：解耦与可插拔

```
main.py（评测框架）
   │  只认统一接口 run_agent()
   ▼
agent_adapter.py（被测系统适配层）
   │  mode="mock" → mock_run_agent()   快速回归
   │  mode="real" → real_run_agent()   真实链路
   ▼
被测 Agent（Mock 字典 / 真实 LLM Agent）
```

**核心收益**：切换被测对象只改 `AGENT_MODE` 一个变量（`main.py:9`），评测框架与 Checker 一行不动。已实测双向切换：
- `"real"` → TC-SEC-001 走真实链路，出 Pass
- `"mock"` → 立刻退回模拟结果

> 面试话术："评测框架和被测系统做了**解耦**，通过统一接口调用 Agent，底层可替换为 Mock 或真实 Agent，切换只改配置，评测逻辑完全复用。"

---

## 五、工程化

- **回归测试**：`test_trace_checker.py` 用 pytest 给 4 个 Checker 各写正例/反例，10 条全绿。先验证"尺子本身准不准"，再去量 Agent。
- **评测指标**：`metrics_demo.py` 实现准确率/精确率/召回率/F1，并区分**误放 FP**（放过坏结果，危险）与**误杀 FN**（冤枉好结果）。项目里的 TC-TRACE-001 就是一次真实误杀案例。
- **结果持久化**：运行结果回写 xlsx，形成可追溯报告。

> 面试话术："我不只看通过率，而是拆出误放和误杀——评测的目标不是刷高分，而是不让坏结果漏过去。"

---

## 六、文件结构说明

### 核心文件（面试重点看这些）
| 文件 | 作用 |
|---|---|
| `main.py` | 主框架入口，模块识别 → 路由 Checker → 汇总报告 → 回写 xlsx |
| `agent_adapter.py` | 被测系统适配层，mock/real 模式切换 |
| `batch_checker.py` | 结果评测的各类 Checker 函数 |
| `trace_checker.py` | 过程评测的 4 个 Trace 检查点 |
| `real_agent.py` | 真实 LLM Agent（被测对象） |
| `answer_extractor.py` | 单条场景的提取层（自然语言 → 结构化字段） |
| `batch_e2e.py` | 批量真实评测 + 可配置提取层 |
| `test_trace_checker.py` | 回归测试 |
| `metrics_demo.py` | 评测指标计算 |
| `机票Agent测试用例_30条.xlsx` | 用例数据源 |

### 辅助/探索文件
`deepseek_test.py`、`judge_consistency.py`、`judge_probe.py`、`test_cases.json` 用于元评测；`read_excel.py`、`write_excel.py`、`batch_write_excel.py`、`批量统计.py` 等是 Excel 读写工具脚本。

---

## 七、诚实的边界（面试务必主动说明）

- 主框架 31 条用例中，目前约 10 条有 Checker 判定，其余为"未配置"——这是后续补齐方向。
- 大部分用例的被测结果仍是 mock 字典；**真实链路目前覆盖 3 条安全用例（SEC-001/002/003）**。
- 项目是**方法论完整的教学/面试作品**，不是生产级系统。它的价值在于讲清楚"为什么这样设计"，而不是规模。

---

*最后更新：2026-11-21*
