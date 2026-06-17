from __future__ import annotations


SYSTEM_PROMPT = """You are an expert English reading instructor for Korean students preparing for the Korean CSAT and TOEFL.
Analyze with academic precision.
Return only valid JSON.
Do not include markdown outside JSON.
Explanations should be in Korean.
English examples should remain in English.
Focus on vocabulary, grammar, sentence structure, logical structure, translation, and study questions.
Do not return null values. Use empty strings or empty arrays when information is not available.
Follow the requested JSON keys exactly."""


def build_user_prompt(text: str) -> str:
    return f"""Analyze the following English passage or sentence for Korean learners.

Required output:
1. Estimate the reading level.
2. Extract key vocabulary and explain each item.
3. Analyze each sentence structurally.
4. Explain the logical structure.
5. Generate exactly five study questions:
   - vocabulary
   - grammar
   - inference
   - main idea
   - structure

English text:
{text}"""
