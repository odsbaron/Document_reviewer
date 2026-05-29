# Document Logic and Inside-Knowledge Review SOP

## Objective

审查文档是否逻辑自洽，是否依赖未说明的内部知识，是否泄露非公开或敏感信息。

## Inputs

- 待审查文档：Markdown、TXT、PDF 或 DOCX。
- 公开参考资料：允许用于交叉验证的公开材料。
- 敏感清单：内部代号、客户名、未公开指标、保密字段、隐私字段、密钥模式等。

## Required Checks

### Logic

- Agent MUST flag internal contradictions.
- Agent MUST flag conclusions that are stronger than the evidence.
- Agent MUST flag undefined concepts that affect reasoning.
- Agent MUST flag timeline conflicts and causal jumps.
- Agent SHOULD ignore wording preferences unless they change meaning.

### Inside Knowledge

- Agent MUST flag hidden premises that require private context.
- Agent MUST flag internal codenames without definition or disclosure permission.
- Agent MUST flag unpublished data, customer details, transaction details, security details, credentials, and private metrics.
- Agent MUST mark uncertain sensitive findings for human review.

### Data Consistency

- Agent MUST check figures, percentages, dates, units, and table/body agreement.
- Agent MUST flag missing data sources when claims rely on numbers.

### External Reader

- Agent MUST evaluate whether an external reader can understand and verify the claim from the document plus public sources.
- Agent MUST flag vague references such as "the previous incident", "the plan", or "the old process" when context is missing.

## Output

Every finding MUST include:

- Location
- Excerpt
- Issue type
- Severity
- Reason
- Recommendation
- Human-review flag
