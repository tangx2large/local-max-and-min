# English Reading Analyzer

Korean CSAT and TOEFL learners can paste an English passage and receive structured reading analysis: estimated level, vocabulary, sentence structure, logical structure, Korean translation, and study questions.

## Features

- Streamlit web UI in Korean
- Mobile-friendly layout
- OpenAI API powered analysis
- JSON Schema validation and fallback JSON parser
- Vocabulary table plus detail expanders
- Sentence-by-sentence analysis
- Logical structure summary
- JSON download button
- No database and no permanent user text storage
- Supports Streamlit Secrets and temporary user-provided API keys

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Create `.env` for local use:

```bash
OPENAI_API_KEY=your_api_key_here
```

## Streamlit Cloud Deployment

1. Deploy this repository on Streamlit Community Cloud.
2. Main file path: `app.py`
3. Add this secret in Streamlit app settings:

```toml
OPENAI_API_KEY = "your_api_key_here"
```

If no server-side secret is configured, users can enter a temporary OpenAI API key in the sidebar. The temporary key is not saved permanently by the app.

## Files

```text
.streamlit/config.toml
.streamlit/secrets.toml.example
app.py
analyzer.py
prompts.py
schemas.py
requirements.txt
runtime.txt
tests/test_schema.py
```
