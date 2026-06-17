from __future__ import annotations

from typing import Any


EXPECTED_TOP_LEVEL_KEYS = {
    "level",
    "vocabulary",
    "sentence_analysis",
    "logical_structure",
    "study_questions",
}


ANALYSIS_JSON_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "level",
        "vocabulary",
        "sentence_analysis",
        "logical_structure",
        "study_questions",
    ],
    "properties": {
        "level": {
            "type": "object",
            "additionalProperties": False,
            "required": ["label", "reason"],
            "properties": {
                "label": {
                    "type": "string",
                    "enum": [
                        "CSAT grade-1 level",
                        "TOEFL intermediate",
                        "TOEFL 100-level",
                        "academic advanced",
                    ],
                },
                "reason": {"type": "string"},
            },
        },
        "vocabulary": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "word",
                    "part_of_speech",
                    "korean_meanings",
                    "meaning_in_context",
                    "derivatives",
                    "synonyms",
                    "antonyms",
                    "common_collocations",
                    "importance",
                    "example_sentence",
                ],
                "properties": {
                    "word": {"type": "string"},
                    "part_of_speech": {"type": "string"},
                    "korean_meanings": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "meaning_in_context": {"type": "string"},
                    "derivatives": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "synonyms": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "antonyms": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "common_collocations": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "importance": {
                        "type": "string",
                        "enum": ["high", "medium", "low"],
                    },
                    "example_sentence": {"type": "string"},
                },
            },
        },
        "sentence_analysis": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "original_sentence",
                    "korean_translation",
                    "core_structure",
                    "main_subject",
                    "main_verb",
                    "object_or_complement",
                    "modifiers",
                    "subordinate_clauses",
                    "grammar_points",
                    "difficult_phrase_explanation",
                ],
                "properties": {
                    "original_sentence": {"type": "string"},
                    "korean_translation": {"type": "string"},
                    "core_structure": {"type": "string"},
                    "main_subject": {"type": "string"},
                    "main_verb": {"type": "string"},
                    "object_or_complement": {"type": "string"},
                    "modifiers": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "subordinate_clauses": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "grammar_points": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "difficult_phrase_explanation": {"type": "string"},
                },
            },
        },
        "logical_structure": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "main_claim",
                "supporting_points",
                "contrast_or_concession",
                "cause_effect_relations",
                "hidden_assumptions",
                "conclusion",
                "paragraph_function",
            ],
            "properties": {
                "main_claim": {"type": "string"},
                "supporting_points": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "contrast_or_concession": {"type": "string"},
                "cause_effect_relations": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "hidden_assumptions": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "conclusion": {"type": "string"},
                "paragraph_function": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["paragraph", "function"],
                        "properties": {
                            "paragraph": {"type": "integer"},
                            "function": {"type": "string"},
                        },
                    },
                },
            },
        },
        "study_questions": {
            "type": "array",
            "minItems": 5,
            "maxItems": 5,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["type", "question", "answer", "explanation_korean"],
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": [
                            "vocabulary",
                            "grammar",
                            "inference",
                            "main idea",
                            "structure",
                        ],
                    },
                    "question": {"type": "string"},
                    "answer": {"type": "string"},
                    "explanation_korean": {"type": "string"},
                },
            },
        },
    },
}
