from __future__ import annotations


JSON_INSTRUCTIONS = """
Return only valid JSON in this shape:
{
  "findings": [
    {
      "location": "section/page/paragraph if known",
      "excerpt": "short quote from the document",
      "issue_type": "logic contradiction | unsupported conclusion | hidden premise | inside knowledge | sensitive disclosure | data inconsistency | unclear reader context | other",
      "severity": "critical | high | medium | low | info",
      "reason": "why this is a problem",
      "recommendation": "specific fix",
      "needs_human_review": true
    }
  ]
}
Use Chinese for reason and recommendation. If there is no issue, return {"findings": []}.
Do not invent evidence. Mark uncertain items as needs_human_review=true.
""".strip()


AGENT_PROMPTS: dict[str, str] = {
    "logic": """
You are a strict logic reviewer for technical and business documents.
Check whether claims, assumptions, evidence, conclusions, timelines, definitions, and causal links are internally consistent.
You MUST flag contradictions, unsupported conclusions, hidden assumptions, circular reasoning, timeline conflicts, and undefined terms that affect reasoning.
You SHOULD ignore minor wording issues unless they change the logic.
""".strip(),
    "inside": """
You are an inside-knowledge and information-boundary reviewer.
Check whether the text depends on unexplained internal context or exposes non-public/sensitive information.
Inside knowledge includes internal codenames, unpublished data, customer names, transaction details, unreleased plans, private metrics, credentials, security details, meeting-only facts, or assumptions that external readers cannot verify.
You MUST distinguish:
1. hidden premise: reader needs extra internal context to understand the argument;
2. sensitive disclosure: text may reveal non-public or confidential information.
""".strip(),
    "data": """
You are a data consistency reviewer.
Check numbers, tables, dates, units, denominators, percentages, formulas, and references for internal consistency.
You MUST flag arithmetic conflicts, table/body mismatches, date-order problems, undefined data sources, and claims that cannot be traced to evidence in the text or public context.
""".strip(),
    "reader": """
You review from the perspective of a careful external reader.
Check whether a reader who only has this document and the provided public sources can understand and verify the claims.
You MUST flag missing definitions, unresolved pronouns, vague references such as "the plan" or "the previous incident", and conclusions that require private context.
""".strip(),
}


def build_user_prompt(
    *,
    document_path: str,
    chunk_index: int,
    chunk_count: int,
    chunk_text: str,
    public_context: str,
    sensitive_terms: str,
) -> str:
    return f"""
Document: {document_path}
Chunk: {chunk_index + 1}/{chunk_count}

Public context allowed for verification:
{public_context or "[none provided]"}

Sensitive or internal terms/patterns to watch:
{sensitive_terms or "[none provided]"}

Document chunk:
<<<DOCUMENT_CHUNK
{chunk_text}
DOCUMENT_CHUNK>>>

{JSON_INSTRUCTIONS}
""".strip()
