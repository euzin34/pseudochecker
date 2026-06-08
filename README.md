# Pseudocode Checker

[![Codecov](https://codecov.io/gh/euzin34/pseudochecker/branch/main/graph/badge.svg)](https://codecov.io/gh/euzin34/pseudochecker)

This project checks CIE 9618-style pseudocode for syntax and semantics and can produce a Python preview.

Top-level layout (important):
- src/        : library source code (tokenizer, parser, checker, transpiler, etc.)
- tests/      : pytest tests and sample buggy code
- web/        : small web UI (flask) for demo
- examples/   : example pseudocode files
- run_web.py  : run the demo web app
- requirements.txt : Python dependencies

Quick start
1. Create venv: python -m venv .venv
2. Activate: .\.venv\Scripts\Activate
3. Install: pip install -r requirements.txt
4. Run tests: python -m pytest -q
5. Run web demo: python run_web.py
