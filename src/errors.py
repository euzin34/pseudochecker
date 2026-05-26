#
# Error handling for CIE 9618 Pseudocode Analyzer
# Includes syntax, semantic, type, and warning errors with detailed reporting

class SyntaxError(Exception):
        # Raised when pseudocode syntax is invalid
    def __init__(self, message, line, column, suggestion=None):
        self.message = message
        self.line = line
        self.column = column
        self.suggestion = suggestion
        self.severity = 'CRITICAL'
        super().__init__(self.message)
    
    def __str__(self):
        error_text = f"\n{'=' * 70}\n"
        error_text += "❌ SYNTAX ERROR\n"
        error_text += f"{'=' * 70}\n"
        error_text += f"📍 Location: Line {self.line}, Column {self.column}\n"
        error_text += f"💬 Description: {self.message}\n"
        if self.suggestion:
            error_text += f"💡 Suggestion: {self.suggestion}\n"
        error_text += f"{'=' * 70}\n"
        return error_text


class SemanticError(Exception):
        # Raised when pseudocode has semantic/logic errors
    def __init__(self, message, line, column, suggestion=None):
        self.message = message
        self.line = line
        self.column = column
        self.suggestion = suggestion
        self.severity = 'ERROR'
        super().__init__(self.message)
    
    def __str__(self):
        error_text = f"\n{'=' * 70}\n"
        error_text += "❌ SEMANTIC ERROR\n"
        error_text += f"{'=' * 70}\n"
        error_text += f"📍 Location: Line {self.line}, Column {self.column}\n"
        error_text += f"💬 Description: {self.message}\n"
        if self.suggestion:
            error_text += f"💡 Suggestion: {self.suggestion}\n"
        error_text += f"{'=' * 70}\n"
        return error_text


class TypeError(Exception):
        # Raised when there are type mismatches
    def __init__(self, message, line, column, suggestion=None):
        self.message = message
        self.line = line
        self.column = column
        self.suggestion = suggestion
        self.severity = 'ERROR'
        super().__init__(self.message)
    
    def __str__(self):
        error_text = f"\n{'=' * 70}\n"
        error_text += "❌ TYPE ERROR\n"
        error_text += f"{'=' * 70}\n"
        error_text += f"📍 Location: Line {self.line}, Column {self.column}\n"
        error_text += f"💬 Description: {self.message}\n"
        if self.suggestion:
            error_text += f"💡 Suggestion: {self.suggestion}\n"
        error_text += f"{'=' * 70}\n"
        return error_text


class WarningError(Exception):
        # Raised for non-critical issues that should be brought to attention
    def __init__(self, message, line, column, suggestion=None):
        self.message = message
        self.line = line
        self.column = column
        self.suggestion = suggestion
        self.severity = 'WARNING'
        super().__init__(self.message)
    
    def __str__(self):
        error_text = f"\n{'=' * 70}\n"
        error_text += "⚠️  WARNING\n"
        error_text += f"{'=' * 70}\n"
        error_text += f"📍 Location: Line {self.line}, Column {self.column}\n"
        error_text += f"💬 Description: {self.message}\n"
        if self.suggestion:
            error_text += f"💡 Suggestion: {self.suggestion}\n"
        error_text += f"{'=' * 70}\n"
        return error_text


class ErrorCollector:
        # Collects multiple errors to report them all at once
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def add_error(self, error):
                # Add an error to the collection
        if error.severity == 'WARNING':
            self.warnings.append(error)
        else:
            self.errors.append(error)
    
    def has_errors(self):
                # Check if there are any errors (not warnings)
        return len(self.errors) > 0
    
    def has_warnings(self):
                # Check if there are any warnings
        return len(self.warnings) > 0
    
    def get_all(self):
                # Get all errors and warnings sorted by line number
        all_issues = self.errors + self.warnings
        return sorted(all_issues, key=lambda e: (e.line, e.column))
    
    def clear(self):
                # Clear all collected errors and warnings
        self.errors = []
        self.warnings = []
    
    def report(self):
                # Generate a formatted report of all errors and warnings
        if not self.has_errors() and not self.has_warnings():
            return None
        
        report = "\n" + "=" * 70 + "\n"
        report += "📋 ERROR REPORT\n"
        report += "=" * 70 + "\n"
        
        if self.has_errors():
            report += f"\nFound {len(self.errors)} error(s):\n"
            for i, error in enumerate(self.errors, 1):
                report += f"\n{i}. {type(error).__name__} at Line {error.line}, Column {error.column}\n"
                report += f"   {error.message}\n"
                if error.suggestion:
                    report += f"   💡 {error.suggestion}\n"
        
        if self.has_warnings():
            report += f"\nFound {len(self.warnings)} warning(s):\n"
            for i, warning in enumerate(self.warnings, 1):
                report += f"\n{i}. Warning at Line {warning.line}, Column {warning.column}\n"
                report += f"   {warning.message}\n"
                if warning.suggestion:
                    report += f"   💡 {warning.suggestion}\n"
        
        report += "\n" + "=" * 70 + "\n"
        return report
