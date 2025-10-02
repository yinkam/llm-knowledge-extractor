# LLM Knowledge Extractor

This is a knowledge extractor system built with a **simplified Clean Architecture** using **Python / FastAPI**, **Async SQLite**, and **OpenRouter(Grok LLM)**.

---

## Design Choices and Trade-offs

The code utilizes a **simplified Clean Architecture** to enforce testability and separation of concerns, prioritizing a robust core domain. This setup was fast to implement by leveraging a **project template**. The **asynchronous stack (FastAPI, Aiosqlite)** was chosen for its **best practice performance** and **familiarity**, maximizing API throughput. We use the **OpenRouter** API gateway with the **Grok free tier** to ensure the service is verifiable and runs without cost. The **Knowledge Extractor** was built using simple heuristics to identify noun via stop words. The primary **trade-off** was limiting **robust error handling and logging** and unit testing to simple extractor checks, as the **time required to implement comprehensive async tests** would have prevented feature completion. Search uses a **substring matching** to minimize implementation time since exact matching wasn't required.

---

## Core Technologies

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Framework** | **FastAPI** | High-performance, asynchronous API. |
| **ORM** | **SQLAlchemy 2.0 (Async)** | Database interactions. |
| **Database** | **SQLite + Aiosqlite** | Zero-setup development database. |
| **LLM Interface** | **OpenRouter** | API for easy switching between LLMs (Gemini, GPT). |

---

## Setup and Run Instructions

### Prerequisites

-   Docker
-   Python 3.12+

### Setup

1.  **Clone the repository & create `.env`:**
    ```bash
    git clone [https://github.com/yinkam/llm-knowledge-extractor.git](https://github.com/yinkam/llm-knowledge-extractor.git)
    cd llm-knowledge-extractor
    cp .env.example .env
    # Add your OPENROUTER_API_KEY to the .env file
    ```

2.  **Run with Docker:**
    ```bash
    docker compose up --build
    ```
    The API will be available at `http://localhost:9000`.

---

## Endpoints & Example

| Method | Path | Description |
| :--- | :--- | :--- |
| **`POST`** | `/api/analyze` | Submits text for analysis and saves it. |
| **`GET`** | `/api/search?topic=...` | Searches all analyses for matching `topic` or `keyword`. |

### Example

```bash
curl -X 'POST' \
  'http://localhost:9000/api/analyze' \
  -H 'Content-Type: application/json' \
  -d '{
  "content": "The quick brown fox jumps over the lazy dog. The dog is very lazy."
}'
```

```bash
curl -X 'GET' \
  'http://localhost:9000/api/search?topic=lazy' \
  -H 'Content-Type: application/json'
```