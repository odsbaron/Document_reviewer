# Document_reviewer

Doc Logic Review Agent 是一个轻量的多 Agent 文档审查工具，用 OpenAI-compatible Chat Completions 接口检查：

- 文档内部逻辑是否自洽
- 是否存在证据不足、跳步推理、概念不一致
- 是否依赖未解释的 inside knowledge
- 是否疑似泄露内部代号、客户信息、未公开指标、漏洞细节、密钥等敏感信息

如需在本地查看参考项目，可以放在 `external/`。该目录是本地参考资料目录，不会提交到 GitHub：

- `external/document_ai_agents`
- `external/agent-sop`
- `external/ai-code-reviewer`

可选拉取命令：

```powershell
mkdir external
git clone --depth 1 https://github.com/CVxTz/document_ai_agents.git .\external\document_ai_agents
git clone --depth 1 https://github.com/strands-agents/agent-sop.git .\external\agent-sop
git clone --depth 1 https://github.com/calimero-network/ai-code-reviewer.git .\external\ai-code-reviewer
```

本项目主体是独立实现，默认按 AIHubMix 的 OpenAI-compatible 接口运行。

默认配置：

- Base URL: `https://aihubmix.com/v1`
- Model: `gpt-4o-mini`
- Keyring service: `aihubmix`
- Keyring username: `sjqy`

## Install

PowerShell:

```powershell
cd F:\Quant\因子\基本面因子\doc_logic_review_agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

## Store API Key

第一次使用时，把 AIHubMix API key 写入系统 keyring：

```powershell
.\.venv\Scripts\doc-review-agent.exe store-key
```

命令会隐藏输入你的 API key，并写入：

- service: `aihubmix`
- username: `sjqy`

之后运行审查时不需要在 `.env` 里保存明文密钥。

如果想用命令行一次性写入：

```powershell
.\.venv\Scripts\doc-review-agent.exe store-key --key sk-你的key
```

## Optional Configuration

通常不需要 `.env`。如果要换模型或备用地址，可以复制示例配置：

```powershell
Copy-Item .env.example .env
notepad .env
```

AIHubMix 文档给出的 OpenAI-compatible 地址是：

```env
AIHUBMIX_BASE_URL=https://aihubmix.com/v1
AIHUBMIX_MODEL=gpt-4o-mini
```

也兼容传统 OpenAI 环境变量：

```env
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://aihubmix.com/v1
OPENAI_MODEL=gpt-4o-mini
```

## Inspect Without API

先确认文档能被读取和切块：

```powershell
python -m doc_review_agent.cli inspect .\samples\sample_document.md
```

## Review

```powershell
python -m doc_review_agent.cli review .\samples\sample_document.md `
  --public-source .\samples\public_context.md `
  --sensitive-list .\samples\sensitive_terms.txt `
  --out review_report.md
```

试跑时可以限制只审第一个 chunk，节省 token：

```powershell
python -m doc_review_agent.cli review .\samples\sample_document.md `
  --public-source .\samples\public_context.md `
  --sensitive-list .\samples\sensitive_terms.txt `
  --out review_report.md `
  --max-chunks 1
```

也可以直接传入配置覆盖 `.env`：

```powershell
python -m doc_review_agent.cli review .\your_doc.pdf `
  --api-key sk-xxx `
  --base-url https://your-compatible-endpoint/v1 `
  --model your-model-name
```

但推荐方式仍然是 keyring，不在命令历史里留下 key。

## Agents

默认运行四个 Agent：

- `logic`：逻辑矛盾、证据不足、因果跳步、概念不一致
- `inside`：inside knowledge、隐藏前提、敏感/非公开信息
- `data`：数字、日期、表格、单位、引用来源一致性
- `reader`：外部读者是否能理解和验证

只运行指定 Agent：

```powershell
python -m doc_review_agent.cli review .\your_doc.md --agent logic --agent inside
```

## Output

输出是 Markdown 报告，包含：

- 问题位置
- 原文摘录
- 问题类型
- 严重等级
- 判断理由
- 修改建议
- 是否需要人工复核

## Deployment

本项目是本地 CLI 工具，推荐部署方式是 Python 虚拟环境加系统 keyring：

```powershell
git clone git@github.com:odsbaron/Document_reviewer.git
cd Document_reviewer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
.\.venv\Scripts\doc-review-agent.exe store-key
```

`store-key` 会把 AIHubMix API key 写入系统 keyring：

- service: `aihubmix`
- username: `sjqy`

API key 不需要写入 `.env`，也不应提交到 Git。默认接口配置为：

```env
AIHUBMIX_BASE_URL=https://aihubmix.com/v1
AIHUBMIX_MODEL=gpt-4o-mini
```

部署后运行：

```powershell
.\.venv\Scripts\doc-review-agent.exe review .\samples\sample_document.md `
  --public-source .\samples\public_context.md `
  --sensitive-list .\samples\sensitive_terms.txt `
  --out review_report.md
```
