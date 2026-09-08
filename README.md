# Fact Knowledge Layer
A lightweight, local LLM based system that extracts facts from PDF documents, stores them, and automatically discovers corroborations, contradictions, and reconciled facts across multiple documents exactly as required by the Engineering Intern Hiring Assignment.
The system is designed to run entirely offline on a standard laptop (no GPU required) using Ollama and a compact Llama 3.2 (3B) model. It provides a Streamlit UI for uploading PDFs and inspecting the results.

---

## Setup and Run Instructions

### Prerequisites
- **Python 3.10+**
- **Ollama** – [Download and install](https://ollama.com)
- **Git** (to clone the repository)

### Step‑by‑Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/fact-knowledge-layer.git
   cd fact-knowledge-layer
   
2. **Create and activate a Python virtual environment**
   ```bash
   python -m venv venv
    # Windows:
    venv\Scripts\activate
    # macOS / Linux:
    source venv/bin/activate
   
3. **Install required packages**
    ```bash
    pip install -r requirements.txt

4. **Pull the language model**
    ```bash
    ollama pull llama3.2:3b

5. **Start the Ollama server** (keep this terminal window open)
   ```bash
   ollama serve
   
6. **Launch the Streamlit app** (in a new terminal, with the virtual environment active)
   ```bash
   streamlit run app.py

## Video Demo
https://drive.google.com/file/d/15VuBjyBDbVg28vVYdnWXC-UdvK5Wb3qU/view?usp=sharing

## How It Works

- **Extraction**: `pdfplumber` reads text → chunked → Ollama + `llama3.2:3b` extracts facts as JSON (entity, attribute, value, unit, period, etc.).
- **Storage**: local JSON file with document metadata.
- **Relationships**: pairwise comparison across documents:
  - **Corroboration**: same entity/attribute, numeric values within 10%.
  - **Contradiction**: same entity/attribute, values differ >30%.
  - **Reconciled**: values differ but explained by different time periods, units, or scope.
- **UI**: Streamlit tabs for extracted facts, four cases, and full fact table.

## Key Choices & Trade‑offs

- **Local LLM** over API – no rate limits, no cost, fully offline.
- **Simple JSON storage** – portable, but not scalable to thousands of facts.
- **Rule‑based matching** – easy to interpret, but misses semantic paraphrases.
- **Minimal prompt + `format:json`** – keeps responses parseable.

## Limitations & Next Steps

- Extraction quality varies; some facts may be missed or malformed.
- No incremental updates – re‑extracts all new documents from scratch.
- No semantic similarity – relies on exact entity/attribute strings.
- **Next**: vector embeddings, graph DB, incremental processing, better error recovery.

## Four Cases (UI Tab)

The app displays examples of all four required cases once you upload at least two PDFs:
1. Corroboration (e.g., similar GDP growth figures)
2. Contradiction (e.g., different inflation rates)
3. Reconciled by context (e.g., different fiscal years)
4. Extraction failure (example included in code)
