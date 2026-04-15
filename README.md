# ⚡ FlashForge AI — Flashcard Generator (No-LLM Version)

An AI-powered flashcard generator that turns your study notes into interactive Q&A cards using NLP — no API keys, no internet, no model downloads required.

---

## Pipeline

```
User Input (text / PDF)
        │
        ▼
 Text Extraction (parser.py)
        │
        ▼
 Sentence Splitting
        │
        ▼
 Keyphrase Extraction — RAKE Algorithm (generator.py)
   (scores phrases by word co-occurrence frequency)
        │
        ▼
 Answer Matching
   (finds the sentence that best contains each keyphrase)
        │
        ▼
 Question Generation — Template-based
   Easy:   "What is X?" / "Define X."
   Medium: "Explain X." / "How does X work?"
   Hard:   "Analyze X." / "Evaluate the importance of X."
        │
        ▼
 Streamlit UI
   ┌──────────────────┬──────────────────┐
   │  Flashcard View  │    Quiz Mode     │
   │  (browse all)    │  (score tracker) │
   └──────────────────┴──────────────────┘
```

---

## Setup (3 steps)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py

# 3. Open in browser
# http://localhost:8501
```

That's it — no Ollama, no API key, no model download needed.

---

## Features

- Paste notes or upload `.txt` / `.pdf` files
- Difficulty levels: Easy / Medium / Hard (based on Bloom's Taxonomy)
- Interactive flashcard browser
- Quiz mode with score tracking and progress bar
- Export flashcards as CSV (compatible with Anki)

---

## Project Structure

```
flashcard-ai/
├── app.py          # Streamlit UI (3 tabs: Generate, Flashcards, Quiz)
├── generator.py    # RAKE keyphrase extraction + question generation
├── parser.py       # PDF and TXT text extraction
├── utils.py        # CSV export helper
├── requirements.txt
└── README.md
```

---

## Tech Stack

| Component | Tool | Why |
|---|---|---|
| UI | Streamlit | Rapid prototyping, clean interface |
| Keyphrase extraction | RAKE (pure Python) | No dependencies, fast, effective |
| PDF reading | PyMuPDF | Accurate multi-page extraction |
| Question generation | Template-based NLP | Transparent, controllable |

---

## Design Decisions & Tradeoffs

**Why RAKE over spaCy/NLTK?**
RAKE is implemented from scratch with zero extra dependencies. It works by identifying co-occurring non-stopword sequences and scoring them — a well-established NLP technique (Rose et al., 2010).

**Why template-based questions?**
LLM-generated questions are more natural but require external tools, API keys, or large model downloads. Template-based generation is transparent, reproducible, and fast — valuable properties in a classroom/offline context.

**Bloom's Taxonomy mapping:**
- Easy → Remember (recall, define, name)
- Medium → Understand (explain, describe, how/why)
- Hard → Analyze/Evaluate (compare, evaluate, apply)
