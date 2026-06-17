from __future__ import annotations

import json
import os
import re
from typing import Any

from dotenv import load_dotenv
from jsonschema import ValidationError, validate
from openai import APIConnectionError, AuthenticationError, OpenAI, OpenAIError, RateLimitError

from prompts import SYSTEM_PROMPT, build_user_prompt
from schemas import ANALYSIS_JSON_SCHEMA, EXPECTED_TOP_LEVEL_KEYS


DEFAULT_MODEL = "gpt-4o-mini"


class AnalysisError(Exception):
    """Raised when the passage cannot be analyzed for a user-facing reason."""


def _get_api_key() -> str | None:
    env_api_key = os.getenv("OPENAI_API_KEY")
    if env_api_key:
        return env_api_key

    try:
        import streamlit as st

        return st.secrets.get("OPENAI_API_KEY")
    except Exception:
        return None


def _validate_analysis(data: dict[str, Any]) -> None:
    missing_keys = EXPECTED_TOP_LEVEL_KEYS - data.keys()
    if missing_keys:
        missing = ", ".join(sorted(missing_keys))
        raise AnalysisError(f"분석 결과에 필요한 항목이 없습니다: {missing}")

    try:
        validate(instance=data, schema=ANALYSIS_JSON_SCHEMA)
    except ValidationError as exc:
        path = " > ".join(str(part) for part in exc.absolute_path) or "최상위"
        raise AnalysisError(
            f"AI 응답 형식이 예상과 다릅니다. 문제가 있는 위치: {path}. 다시 시도해 주세요."
        ) from exc


def _strip_code_fence(content: str) -> str:
    text = content.strip().lstrip("\ufeff")
    fenced_match = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL)
    if fenced_match:
        return fenced_match.group(1).strip()
    return text


def _extract_json_object(content: str) -> dict[str, Any] | None:
    decoder = json.JSONDecoder()
    text = _strip_code_fence(content)

    for start_index, char in enumerate(text):
        if char != "{":
            continue
        try:
            parsed, _ = decoder.raw_decode(text[start_index:])
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed

    return None


def _parse_json(content: str) -> dict[str, Any]:
    cleaned_content = _strip_code_fence(content)

    try:
        data = json.loads(cleaned_content)
    except json.JSONDecodeError:
        data = _extract_json_object(content)
        if data is None:
            raise AnalysisError(
                "AI 응답을 JSON으로 해석하지 못했습니다. 잠시 후 다시 시도하거나 입력 지문을 조금 줄여 주세요."
            )

    if not isinstance(data, dict):
        raise AnalysisError("AI 응답 형식이 올바르지 않습니다. 다시 시도해 주세요.")

    _validate_analysis(data)
    return data


def analyze_text(text: str, api_key_override: str | None = None) -> dict[str, Any]:
    cleaned_text = text.strip()
    if not cleaned_text:
        raise AnalysisError("분석할 영어 지문을 입력해 주세요.")

    load_dotenv()
    api_key = api_key_override or _get_api_key()
    if not api_key:
        raise AnalysisError(
            ".env, Streamlit secrets, 또는 임시 API 키가 없습니다. API 키를 설정한 뒤 다시 실행해 주세요."
        )

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(cleaned_text)},
            ],
            temperature=0.2,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "english_reading_analysis",
                    "schema": ANALYSIS_JSON_SCHEMA,
                    "strict": True,
                },
            },
        )
    except AuthenticationError as exc:
        raise AnalysisError(
            "OpenAI API 키를 인증하지 못했습니다. 입력한 API 키 또는 배포 Secrets를 확인해 주세요."
        ) from exc
    except RateLimitError as exc:
        raise AnalysisError(
            "OpenAI API 사용량 한도 또는 속도 제한에 도달했습니다. 잠시 후 다시 시도해 주세요."
        ) from exc
    except APIConnectionError as exc:
        raise AnalysisError(
            "OpenAI 서버에 연결하지 못했습니다. 인터넷 연결 상태를 확인한 뒤 다시 시도해 주세요."
        ) from exc
    except OpenAIError as exc:
        raise AnalysisError(f"OpenAI API 호출 중 오류가 발생했습니다: {exc}") from exc

    content = response.choices[0].message.content
    if not content:
        raise AnalysisError("OpenAI API가 빈 응답을 반환했습니다. 다시 시도해 주세요.")

    return _parse_json(content)
