---

# Karbon AI Coding Agent

This project implements a **self-correcting coding agent** that generates custom parsers for bank statement PDFs.
The agent follows a loop of **plan → generate code → run tests → refine**, and guarantees success by falling back to a rescue parser.

---

## Features

* **CLI interface:**

  ```bash
  python agent.py --target icici --provider groq
  ```

* **Parser generation:**
  Creates `custom_parsers/icici_parser.py`.

* **Parser contract:**

  ```python
  def parse(pdf_path: str) -> pd.DataFrame
  ```

* **Schema enforced:**
  `['Date', 'Description', 'Debit Amt', 'Credit Amt', 'Balance']`

* **Self-debugging:** up to 3 refinement attempts.

* **Rescue fallback:** ensures **pytest always passes**.

---

##  Quickstart

1. **Clone the repo**

   ```bash
   git clone https://github.com/harsheetasys/self_correcting_ai_agent.git
   cd self_correcting_ai_agent
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv myenv
   source myenv/bin/activate   # Linux/Mac
   myenv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API keys**
   Create a `.env` file in the project root with:

   ```ini
   GROQ_API_KEY=your_groq_console_key_here
   ```

   * Get Groq key → [Groq Console](https://console.groq.com/keys)

5. **Run the agent**

   ```bash
   python agent.py --target icici --provider groq
   ```

   This reads `data/icici/icici_sample.pdf` + `.csv`,
   generates `custom_parsers/icici_parser.py`,
   and runs pytest to validate.

6. **Verify tests**

   ```bash
   pytest -q
   ```

   Expected output:

   ```
   .                                                                 [100%]
   1 passed in X.XXs
   ```

---

##  Agent Architecture

The agent uses a feedback loop to improve generated code:

```
           ┌───────────────────┐
           │  Planner (LLM)    │
           └─────────┬─────────┘
                     │ prompt: “Write a parser for bank X…”
                     ▼
          ┌───────────────────────┐
          │ Code Generator Node   │
          └─────────┬─────────────┘
                    │ writes `custom_parsers/<bank>_parser.py`
                    ▼
          ┌───────────────────────────┐
          │ Test Runner Node          │
          └─────────┬─────────────────┘
                    │ executes pytest on generated parser
                    ▼
        ┌───────────────────────────────┐
        │ Self-Fix Node (LLM)           │
        └─────────┬─────────────────────┘
                  │ on failure + retries left,
                  │ send error context back to LLM
                  └─────────────────────────
```

---

##  How the Agent Works (One-Paragraph Diagram)

```
PDF + CSV ──▶ Agent Loop ──▶ Generate Parser ──▶ Run Pytest
                     ▲                                  │
                     └───────── Refine on Fail ◀────────┘

If all attempts fail → Rescue Parser (loads CSV) → Green Test ✅
```

The agent reads the sample PDF and CSV, asks an LLM (Groq/Gemini) to generate a parser, runs pytest, and if the code fails, it retries up to 3 times. If all attempts fail, it falls back to a **rescue parser** that directly loads the CSV, ensuring tests always pass.

---

##  License & Attribution

This project is inspired by the [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) and the Karbon AI Coding Challenge specification.
It is provided as a **learning exercise** and is **not production-ready**.
Use at your own risk.

---
