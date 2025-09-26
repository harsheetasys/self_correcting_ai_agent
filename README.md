# Karbon AI Challenge – Agent‑as‑Coder

Welcome to the **Agent‑as‑Coder** coding assignment.  This project asks you
to build a small autonomous agent capable of generating custom PDF parsers for
bank statements.  The agent takes a sample statement (PDF) and the expected
CSV output and, via an LLM, writes a parser that can convert similar
statements into a tabular dataframe.  The agent iterates on its own output
until the generated parser passes a test suite.

## 📂 Project layout

```text
karbon_ai_challenge/
├── agent.py            # Main entry point for running the agent
├── custom_parsers/     # Auto‑generated parsers live here
│   ├── __init__.py
│   └── base_parser.py  # Abstract base class for all parsers
├── data/               # Sample PDFs and their corresponding CSVs
│   └── …
├── tests/
│   └── test_parser.py  # Validation of generated parser output
├── README.md           # You’re reading it!
└── requirements.txt    # Python dependencies
```

## ✅ How to run the agent

1. **Install dependencies**

   From a fresh clone, create a virtual environment and install the
   requirements:

   ```bash
   cd karbon_ai_challenge
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Set your API key**

   The agent uses a large language model to generate code.  Export an OpenAI
   API key (or Gemini / Groq credentials) before running:

   ```bash
   export OPENAI_API_KEY=sk-...
   ```

   The script currently defaults to the OpenAI API.  See `agent.py` for how
   to plug in alternative providers.

3. **Prepare your data**

   Place the sample PDF and its corresponding CSV in a subdirectory under
   `data/` named after the target bank.  For example:

   ```text
   data/
   └── icici/
       ├── icici_sample.pdf
       └── icici_sample.csv
   ```

4. **Run the agent**

   Invoke the agent from the command line, specifying the bank name via
   `--target`:

   ```bash
   python agent.py --target icici
   ```

   The agent will:
   - Read the sample PDF and CSV
   - Ask the LLM to write a new parser (`custom_parsers/icici_parser.py`)
   - Run the parser against the sample data
   - Iterate up to three times to fix any failing tests
   - Exit once the parser passes

5. **Run the tests**

   After the agent has created the parser you can verify correctness with
   pytest:

   ```bash
   pytest -q
   ```

## 🔧 Agent architecture

The agent follows a simple **plan → code → test → refine** loop inspired by
Anthropic‑style tool use.  Here’s a high‑level overview:

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
                    │ executes tests in `tests/`
                    │ returns success or failure
                    ▼
        ┌───────────────────────────────┐
        │ Self‑Fix Node (LLM)          │
        └─────────┬─────────────────────┘
                  │ if failures remain and retries < 3,
                  │ send error context back to the LLM
                  │ for code refinement
                  └─────────────────────────

The loop halts when either the parser passes all tests or the maximum number
of attempts (three by default) is exhausted.  During each iteration the
agent stores intermediate artifacts (e.g. prompts, generated code) in a
temporary directory for transparency and traceability.

## 📜 License and attribution

This project is a derivative work inspired by the [mini‑swe‑agent](https://github.com/SWE-agent/mini-swe-agent)
and the Karbon AI coding challenge specification.  It is provided as a
learning exercise and does not include production‑grade error handling or
security features.  Use at your own risk.
