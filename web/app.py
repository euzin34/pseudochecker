#
# Flask web application for Pseudochecker.

import os
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template, request

PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Ensure project root is on sys.path so 'src' package can be imported when running this file directly
sys.path.insert(0, str(PROJECT_ROOT))

from src.checker import PseudocodeChecker

EXAMPLES_DIR = PROJECT_ROOT / "examples"
DOCS_DIR = PROJECT_ROOT / "docs"


def create_app():
    app = Flask(
        __name__,
        template_folder=str(Path(__file__).parent / "templates"),
        static_folder=str(Path(__file__).parent / "static"),
    )

    checker = PseudocodeChecker(
        treat_warnings_as_failure=False,
        include_python_preview=True,
    )

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/reference")
    def reference():
        quick_ref = DOCS_DIR / "QUICK_REFERENCE.md"
        content = ""
        if quick_ref.exists():
            content = quick_ref.read_text(encoding="utf-8")
        return render_template("reference.html", reference_content=content)

    @app.route("/api/check", methods=["POST"])
    def api_check():
        data = request.get_json(silent=True) or {}
        source = data.get("source", "")
        if not source.strip():
            return jsonify(
                {
                    "ok": False,
                    "errors": [
                        {
                            "type": "ValidationError",
                            "severity": "ERROR",
                            "line": 1,
                            "column": 1,
                            "message": "No pseudocode provided.",
                            "suggestion": "Type or paste pseudocode in the editor.",
                        }
                    ],
                    "warnings": [],
                    "stats": {},
                    "python_preview": None,
                    "stage": "input",
                    "message": "Empty input.",
                }
            )

        include_preview = data.get("include_python_preview", True)
        result = PseudocodeChecker(
            treat_warnings_as_failure=False,
            include_python_preview=include_preview,
        ).check(source, filename="editor")
        return jsonify(result.to_dict())

    @app.route("/api/examples")
    def api_examples_list():
        names = []
        if EXAMPLES_DIR.exists():
            names = sorted(
                p.stem for p in EXAMPLES_DIR.glob("*.txt")
            )
        return jsonify({"examples": names})

    @app.route("/api/examples/<name>")
    def api_example(name):
        safe_name = "".join(c for c in name if c.isalnum() or c in ("_", "-"))
        path = EXAMPLES_DIR / f"{safe_name}.txt"
        if not path.exists():
            return jsonify({"error": "Example not found"}), 404
        return jsonify({"name": safe_name, "source": path.read_text(encoding="utf-8")})

    return app


app = create_app()


if __name__ == "__main__":
    # Development entrypoint: run with python web/app.py
    app.run(debug=True, host="127.0.0.1", port=5000)
