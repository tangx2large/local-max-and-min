import json

import pytest

from analyzer import AnalysisError, _parse_json
from schemas import EXPECTED_TOP_LEVEL_KEYS


def sample_response() -> dict:
    questions = [
        {
            "type": question_type,
            "question": "Sample question?",
            "answer": "Sample answer.",
            "explanation_korean": "예시 해설입니다.",
        }
        for question_type in ["vocabulary", "grammar", "inference", "main idea", "structure"]
    ]

    return {
        "level": {
            "label": "TOEFL intermediate",
            "reason": "문장 구조와 어휘가 중급 학술 독해 수준입니다.",
        },
        "vocabulary": [
            {
                "word": "literacy",
                "part_of_speech": "noun",
                "korean_meanings": ["문해력"],
                "meaning_in_context": "글을 맥락 속에서 이해하는 능력",
                "derivatives": ["literate"],
                "synonyms": ["reading ability"],
                "antonyms": ["illiteracy"],
                "common_collocations": ["academic literacy"],
                "importance": "high",
                "example_sentence": "Academic literacy develops through practice.",
            }
        ],
        "sentence_analysis": [
            {
                "original_sentence": "Literacy is shaped by social contexts.",
                "korean_translation": "문해력은 사회적 맥락에 의해 형성된다.",
                "core_structure": "S + be verb + past participle",
                "main_subject": "Literacy",
                "main_verb": "is shaped",
                "object_or_complement": "by social contexts",
                "modifiers": [],
                "subordinate_clauses": [],
                "grammar_points": ["passive voice"],
                "difficult_phrase_explanation": "be shaped by는 '~에 의해 형성되다'라는 뜻입니다.",
            }
        ],
        "logical_structure": {
            "main_claim": "문해력은 단순 해독 능력 이상이다.",
            "supporting_points": ["사회적 맥락이 읽기 방식에 영향을 준다."],
            "contrast_or_concession": "단어를 알아도 주장을 오해할 수 있다.",
            "cause_effect_relations": ["논리 구조를 파악하면 독해 정확도가 높아진다."],
            "hidden_assumptions": ["학술 독해는 구조 파악을 요구한다."],
            "conclusion": "고급 독해 수업은 어휘, 문법, 논리 구조를 함께 다뤄야 한다.",
            "paragraph_function": [{"paragraph": 1, "function": "중심 주장 제시"}],
        },
        "study_questions": questions,
    }


def test_sample_response_has_expected_top_level_keys() -> None:
    assert EXPECTED_TOP_LEVEL_KEYS.issubset(sample_response().keys())


def test_parse_json_accepts_valid_json() -> None:
    parsed = _parse_json(json.dumps(sample_response(), ensure_ascii=False))
    assert parsed["level"]["label"] == "TOEFL intermediate"


def test_parse_json_accepts_fenced_json() -> None:
    content = f"```json\n{json.dumps(sample_response(), ensure_ascii=False)}\n```"
    parsed = _parse_json(content)
    assert parsed["vocabulary"][0]["word"] == "literacy"


def test_parse_json_extracts_json_with_extra_text() -> None:
    content = f"Here is the analysis:\n{json.dumps(sample_response(), ensure_ascii=False)}\nDone."
    parsed = _parse_json(content)
    assert parsed["logical_structure"]["main_claim"]


def test_parse_json_rejects_invalid_schema() -> None:
    invalid = {"level": {"label": "TOEFL intermediate", "reason": "x"}}
    with pytest.raises(AnalysisError):
        _parse_json(json.dumps(invalid, ensure_ascii=False))
