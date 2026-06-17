from __future__ import annotations

import json
from typing import Any

import pandas as pd
import streamlit as st

from analyzer import AnalysisError, analyze_text


SAMPLE_PASSAGE = """In recent decades, researchers have increasingly argued that literacy is not merely the ability to decode written symbols, but a flexible set of practices shaped by social contexts. A student who can identify every word in a scientific article may still misunderstand the author's claim if she fails to recognize how evidence, qualification, and counterargument interact. For this reason, advanced reading instruction should emphasize not only vocabulary and grammar, but also the logical architecture of academic prose."""


st.set_page_config(
    page_title="English Reading Analyzer",
    page_icon="📘",
    layout="wide",
)


def inject_mobile_styles() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1120px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        [data-testid="stTextArea"] textarea {
            font-size: 1rem;
            line-height: 1.55;
        }
        div[data-testid="stButton"] button,
        div[data-testid="stDownloadButton"] button {
            min-height: 2.75rem;
            font-weight: 700;
        }
        div[data-testid="stDataFrame"] {
            overflow-x: auto;
        }
        @media (max-width: 640px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 1.25rem;
            }
            h1 {
                font-size: 1.8rem !important;
                line-height: 1.2 !important;
            }
            h2, h3 {
                line-height: 1.25 !important;
            }
            [data-testid="stTextArea"] textarea {
                min-height: 220px;
            }
            div[data-testid="stButton"] button,
            div[data-testid="stDownloadButton"] button {
                width: 100%;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def join_values(values: list[str] | None) -> str:
    return ", ".join(values or []) or "-"


def render_bullet_list(items: list[str] | None, empty_text: str = "해당 없음") -> None:
    if not items:
        st.write(empty_text)
        return

    for item in items:
        st.write(f"- {item}")


def render_level(level: dict[str, Any]) -> None:
    st.subheader("A. 예상 난이도")
    left, right = st.columns([1, 3])
    with left:
        st.metric("레벨", level.get("label", "분석 불가"))
    with right:
        st.info(level.get("reason", "난이도 설명을 가져오지 못했습니다."))


def render_vocabulary(vocabulary: list[dict[str, Any]]) -> None:
    st.subheader("B. 핵심 어휘")
    if not vocabulary:
        st.info("핵심 어휘 분석 결과가 없습니다.")
        return

    summary_rows = [
        {
            "어휘/표현": item.get("word", ""),
            "품사": item.get("part_of_speech", ""),
            "한국어 뜻": join_values(item.get("korean_meanings")),
            "문맥상 의미": item.get("meaning_in_context", ""),
            "중요도": item.get("importance", ""),
        }
        for item in vocabulary
    ]
    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

    st.markdown("**상세 어휘 설명**")
    for item in vocabulary:
        title = f"{item.get('word', '어휘')} | {item.get('importance', 'importance 없음')}"
        with st.expander(title):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**품사:** {item.get('part_of_speech', '-')}")
                st.markdown(f"**한국어 뜻:** {join_values(item.get('korean_meanings'))}")
                st.markdown(f"**문맥상 의미:** {item.get('meaning_in_context', '-')}")
                st.markdown(f"**파생어:** {join_values(item.get('derivatives'))}")
            with col2:
                st.markdown(f"**동의어:** {join_values(item.get('synonyms'))}")
                st.markdown(f"**반의어:** {join_values(item.get('antonyms'))}")
                st.markdown(f"**자주 쓰는 연어:** {join_values(item.get('common_collocations'))}")
                st.markdown(f"**예문:** {item.get('example_sentence', '-')}")


def render_sentence_analysis(sentences: list[dict[str, Any]]) -> None:
    st.subheader("C. 문장 구조 분석")
    if not sentences:
        st.info("문장 분석 결과가 없습니다.")
        return

    for index, sentence in enumerate(sentences, start=1):
        preview = sentence.get("original_sentence", "")[:90]
        with st.expander(f"문장 {index}: {preview}", expanded=index == 1):
            st.markdown("**원문**")
            st.write(sentence.get("original_sentence", "-"))
            st.markdown("**한국어 해석**")
            st.success(sentence.get("korean_translation", "-"))

            structure_rows = [
                {"항목": "핵심 구조", "내용": sentence.get("core_structure", "-")},
                {"항목": "주어", "내용": sentence.get("main_subject", "-")},
                {"항목": "동사", "내용": sentence.get("main_verb", "-")},
                {"항목": "목적어/보어", "내용": sentence.get("object_or_complement", "-")},
            ]
            st.dataframe(pd.DataFrame(structure_rows), use_container_width=True, hide_index=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**수식어**")
                render_bullet_list(sentence.get("modifiers"))
                st.markdown("**종속절**")
                render_bullet_list(sentence.get("subordinate_clauses"))
            with col2:
                st.markdown("**문법 포인트**")
                render_bullet_list(sentence.get("grammar_points"))
                st.markdown("**어려운 표현 설명**")
                st.write(sentence.get("difficult_phrase_explanation", "-"))


def render_logical_structure(logic: dict[str, Any]) -> None:
    st.subheader("D. 논리 구조")

    st.markdown("**중심 주장**")
    st.info(logic.get("main_claim", "분석 결과가 없습니다."))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**근거**")
        render_bullet_list(logic.get("supporting_points"))
        st.markdown("**대조/양보**")
        st.write(logic.get("contrast_or_concession") or "해당 없음")
    with col2:
        st.markdown("**인과 관계**")
        render_bullet_list(logic.get("cause_effect_relations"))
        st.markdown("**숨은 전제**")
        render_bullet_list(logic.get("hidden_assumptions"))

    st.markdown("**결론**")
    st.success(logic.get("conclusion") or "분석 결과가 없습니다.")

    paragraph_functions = logic.get("paragraph_function", [])
    if paragraph_functions:
        st.markdown("**문단별 기능**")
        st.dataframe(
            pd.DataFrame(paragraph_functions).rename(
                columns={"paragraph": "문단", "function": "기능"}
            ),
            use_container_width=True,
            hide_index=True,
        )


def render_study_questions(questions: list[dict[str, Any]]) -> None:
    st.subheader("E. 학습 문제")
    if not questions:
        st.info("학습 문제 생성 결과가 없습니다.")
        return

    type_labels = {
        "vocabulary": "어휘",
        "grammar": "문법",
        "inference": "추론",
        "main idea": "주제",
        "structure": "구조",
    }
    for index, question in enumerate(questions, start=1):
        question_type = type_labels.get(question.get("type"), question.get("type", "문제"))
        with st.expander(f"{index}. {question_type}: {question.get('question', '')}"):
            st.markdown(f"**정답:** {question.get('answer', '-')}")
            st.markdown(f"**해설:** {question.get('explanation_korean', '-')}")


def render_download(result: dict[str, Any]) -> None:
    json_text = json.dumps(result, ensure_ascii=False, indent=2)
    st.download_button(
        label="분석 결과 JSON 다운로드",
        data=json_text,
        file_name="english_reading_analysis.json",
        mime="application/json",
        use_container_width=True,
    )


def render_result(result: dict[str, Any]) -> None:
    render_download(result)
    render_level(result.get("level", {}))
    render_vocabulary(result.get("vocabulary", []))
    render_sentence_analysis(result.get("sentence_analysis", []))
    render_logical_structure(result.get("logical_structure", {}))
    render_study_questions(result.get("study_questions", []))


inject_mobile_styles()

with st.sidebar:
    st.header("설정")
    temporary_api_key = st.text_input(
        "임시 OpenAI API 키",
        type="password",
        help="배포 Secrets가 없는 경우에만 사용합니다. 입력값은 영구 저장하지 않습니다.",
    )
    st.caption("관리자가 Streamlit Secrets에 API 키를 설정하면 이 입력은 비워도 됩니다.")

st.title("📘 English Reading Analyzer")
st.caption("수능 및 TOEFL 대비를 위한 학술 영어 독해 분석 도구")

text = st.text_area(
    "분석할 영어 지문을 입력하세요.",
    value=SAMPLE_PASSAGE,
    height=260,
)

analyze_clicked = st.button("Analyze", type="primary")

if analyze_clicked:
    if not text.strip():
        st.warning("분석할 영어 문장이나 지문을 입력해 주세요.")
    else:
        with st.spinner("영어 지문을 분석하는 중입니다. 잠시만 기다려 주세요..."):
            try:
                st.session_state["analysis_result"] = analyze_text(
                    text,
                    api_key_override=temporary_api_key.strip() or None,
                )
                st.success("분석이 완료되었습니다.")
            except AnalysisError as error:
                st.session_state.pop("analysis_result", None)
                st.error(str(error))
                st.caption(
                    "문제가 계속되면 API 키, 네트워크 연결, 입력 지문의 길이를 확인해 주세요."
                )

if "analysis_result" in st.session_state:
    st.divider()
    render_result(st.session_state["analysis_result"])
