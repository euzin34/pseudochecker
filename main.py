import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.checker import PseudocodeChecker
from src.utils import read_file_safely, get_file_stats, format_file_stats
from src.constants import (
    APP_NAME,
    APP_SUBTITLE,
    HELP_TEXT,
    ERROR_SEPARATOR,
    INFO_SEPARATOR,
    SUCCESS_MESSAGES,
    PROGRESS_INDICATORS,
    VERSION,
)


def print_header():
    print(ERROR_SEPARATOR)
    print(f"  {APP_NAME} v{VERSION}")
    print(f"  {APP_SUBTITLE}")
    print(ERROR_SEPARATOR)
    print()


def print_help():
    print(HELP_TEXT)
    print("  check <file>   - Validate pseudocode (default: examples/basic_example.txt)")
    print("  run <file>     - Alias for check")
    print("  python <file>  - Validate and show Python preview")
    print("  help           - Show commands")
    print("  exit           - Quit")


def print_result(result, show_python=False):
    if result.errors or result.warnings:
        for issue in result.errors + result.warnings:
            print(
                f"\n[{issue['severity']}] {issue['type']} "
                f"at line {issue['line']}, col {issue['column']}\n"
                f"  {issue['message']}"
            )
            if issue.get("suggestion"):
                print(f"  Suggestion: {issue['suggestion']}")
        print()
        return

    print()
    print(ERROR_SEPARATOR)
    print(SUCCESS_MESSAGES["no_errors"])
    print(ERROR_SEPARATOR)
    print(result.message)
    if show_python and result.python_preview:
        print()
        print("--- Python preview ---")
        print(result.python_preview)


def check_file(filename, show_python=False, strict_warnings=False):
    code, error = read_file_safely(filename)
    if error:
        print(f"\nFile error: {error}\n")
        return False

    print()
    print(f"Analyzing: {filename}")
    print(INFO_SEPARATOR)
    stats = get_file_stats(code)
    print(f"Statistics: {format_file_stats(stats)}")
    print()

    checker = PseudocodeChecker(
        treat_warnings_as_failure=strict_warnings,
        include_python_preview=show_python,
    )
    result = checker.check(code, filename=filename)
    print_result(result, show_python=show_python)
    return result.ok


def main():
    print_header()
    print_help()

    while True:
        try:
            user_input = input(">> ").strip()
            if not user_input:
                continue
            if user_input.lower() == "exit":
                print("\nGoodbye!")
                break
            if user_input.lower() == "help":
                print()
                print_help()
                continue

            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            filename = parts[1].strip() if len(parts) > 1 else "examples/basic_example.txt"

            if command in ("run", "check"):
                check_file(filename)
            elif command == "python":
                check_file(filename, show_python=True)
            else:
                print(f"Unknown command: '{command}'. Type 'help' for commands.")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break


if __name__ == "__main__":
    main()
