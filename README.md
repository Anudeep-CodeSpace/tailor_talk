# TailorTalk - 🚢 Titanic Dataset Chat Agent

---

## Description

A friendly chatbot that can answer user questions in English language and get both text answers and visual representations (charts) about the Titanic Passengers.

---

## Tech-Stack

<table>
    <tr>
        <th>Component</th>
        <th>Technology Used</th>
    </tr>
    <tr>
        <td>
            <strong>Backend</strong>
        </td>
        <td>
            Python with FastAPI
        </td>
    </tr>
    <tr>
        <td>
            <strong>Agent Framework</strong>
        </td>
        <td>
            LangChain
        </td>
    </tr>
    <tr>
        <td>
            <strong>Frontend</strong>
        </td>
        <td>
            Streamlit
        </td>
    </tr>
    <tr>
        <td>
            <strong>LLM</strong>
        </td>
        <td>
            Gemini-2.5<br>OpenAI compatible
        </td>
    </tr>
</table>

---

## Features

- Clean Streamlit UI.
- Accept questions in Natural Language.
- Give clear text responses.
- Create helpful Visualizations (charts).

---

## How to Run? 🏃‍♂️

### 1. Clone the repository

```
git clone https://github.com/Anudeep-CodeSpace/tailor_talk.git
cd tailor_talk
```

### 2. Install UV

Install UV following the [official docs](https://docs.astral.sh/uv/getting-started/installation/)

### 3. Install Required Python version

```
uv python install
```

### 4. Sync Dependencies

```
uv sync
```

### 5. (Optional) Download Dataset

```
uv run python backend/download_dataset.py
```

### 6. Start Backend Server

```
uv run main.py
```

### 7. Run the Streamlit server

```
uv run streamlit run frontend/app.py
```

---

## API EndPoints

### POST /chat

```request.json
{
    "query": <user query in natural language>
}
```

```response.json
{
    "answer": <answer by llm>,
    "image": (Optional) plot devised by the llm
}
```

---
## Live Streamlit URL

[Go to Streamlit UI](https://tailortalk-chatbot.streamlit.app/)

---

## Author

Anudeep Reddy Bandi ([Anudeep-CodeSpace](https://github.com/Anudeep-CodeSpace))

---
