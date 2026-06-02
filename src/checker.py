#
# Unified pseudocode checking API for CLI and web.

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from src.tokenizer import Tokenizer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.transpiler import Transpiler
from src.errors import SyntaxError, SemanticError, TypeError, WarningError, ErrorCollector
from src.utils import get_file_stats
from src import config


@dataclass
class CheckResult:
        # Structured result for CLI and JSON API.

    ok: bool
    errors: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[Dict[str, Any]] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)
    python_preview: Optional[str] = None
    observations: List[Dict[str, Any]] = field(default_factory=list)
    stage: str = "complete"
    message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "errors": self.errors,
            "warnings": self.warnings,
            "stats": self.stats,
            "python_preview": self.python_preview,
            "observations": self.observations,
            "stage": self.stage,
            "message": self.message,
        }


def _issue_dict(error) -> Dict[str, Any]:
    return {
        "type": type(error).__name__,
        "severity": error.severity,
        "line": error.line,
        "column": error.column,
        "message": error.message,
        "suggestion": error.suggestion,
    }


def _collector_to_lists(collector: ErrorCollector):
    errors = [_issue_dict(e) for e in collector.errors]
    warnings = [_issue_dict(w) for w in collector.warnings]
    return errors, warnings


class PseudocodeChecker:
        # Runs tokenize -> parse -> semantic analysis on pseudocode source.

    def __init__(
        self,
        treat_warnings_as_failure: Optional[bool] = None,
        include_python_preview: Optional[bool] = None,
    ):
        self.treat_warnings_as_failure = (
            treat_warnings_as_failure
            if treat_warnings_as_failure is not None
            else config.TREAT_WARNINGS_AS_FAILURE
        )
        self.include_python_preview = (
            include_python_preview
            if include_python_preview is not None
            else config.ENABLE_PYTHON_PREVIEW
        )

    def check(self, source: str, filename: str = "input") -> CheckResult:
        stats = get_file_stats(source)
        stats["filename"] = filename

        if not source.strip():
            return CheckResult(
                ok=False,
                errors=[
                    {
                        "type": "ValidationError",
                        "severity": "ERROR",
                        "line": 1,
                        "column": 1,
                        "message": "No pseudocode provided.",
                        "suggestion": "Type or paste pseudocode in the editor.",
                    }
                ],
                stats=stats,
                stage="input",
                message="Empty input.",
            )

        try:
            tokenizer = Tokenizer(source)
            tokens = tokenizer.tokenize()
            stats["token_count"] = max(0, len(tokens) - 1)

            parser = Parser(tokens)
            ast = parser.parse()
            stats["statement_count"] = len(ast.statements)

            analyzer = SemanticAnalyzer(ast)
            collector = analyzer.analyze()
            errors, warnings = _collector_to_lists(collector)

            has_blocking = bool(errors) or (
                self.treat_warnings_as_failure and bool(warnings)
            )

            python_preview = None
            if self.include_python_preview and not has_blocking:
                try:
                    python_preview = self._build_python_preview(ast)
                except Exception as exc:
                    python_preview = f"# Preview unavailable: {exc}"

            observations = getattr(analyzer, 'observations', [])

            if has_blocking:
                return CheckResult(
                    ok=False,
                    errors=errors,
                    warnings=warnings,
                    stats=stats,
                    python_preview=python_preview,
                    observations=observations,
                    stage="semantic" if errors else "warnings",
                    message="Validation failed.",
                )

            msg = "Pseudocode is valid."
            if warnings:
                msg = "Pseudocode is valid with warnings."

            return CheckResult(
                ok=True,
                errors=errors,
                warnings=warnings,
                stats=stats,
                python_preview=python_preview,
                observations=observations,
                stage="complete",
                message=msg,
            )

        except SyntaxError as exc:
            return CheckResult(
                ok=False,
                errors=[_issue_dict(exc)],
                stats=stats,
                stage="syntax",
                message=str(exc.message),
            )
        except Exception as exc:
            return CheckResult(
                ok=False,
                errors=[
                    {
                        "type": "InternalError",
                        "severity": "CRITICAL",
                        "line": 1,
                        "column": 1,
                        "message": str(exc),
                        "suggestion": "Please report this unexpected error.",
                    }
                ],
                stats=stats,
                stage="internal",
                message=str(exc),
            )

    def _build_python_preview(self, ast) -> str:
        header = (
            "# Generated Python preview (9618 pseudocode)\n"
            "# Not executed — for study only\n"
            "from src.runtime_builtins import *\n\n"
        )
        body = Transpiler().transpile(ast)
        return header + body
