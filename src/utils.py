#
# Utility functions for the pseudocode checker.

def format_error_location(line, column):
        # Format error location for display.
    return f"Line {line}, Column {column}"

def count_lines(code):
        # Count the number of lines in code.
    return len(code.split('\n'))

def get_line_content(code, line_number):
        # Get the content of a specific line.
    lines = code.split('\n')
    if 1 <= line_number <= len(lines):
        return lines[line_number - 1]
    return None

def highlight_error_position(line_content, column):
        # Create a visual indicator for error position.
    if column <= 0 or column > len(line_content):
        return ""
    
    pointer = " " * (column - 1) + "^"
    return f"{line_content}\n{pointer}"

def validate_file_extension(filename):
        # Check if file has a valid extension.
    valid_extensions = ['.txt', '.pseudo', '.psc']
    return any(filename.endswith(ext) for ext in valid_extensions)

def read_file_safely(filename):
        # Read file with error handling.
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read(), None
    except FileNotFoundError:
        return None, f"File '{filename}' not found"
    except PermissionError:
        return None, f"Permission denied to read '{filename}'"
    except Exception as e:
        return None, f"Error reading file: {str(e)}"

def get_file_stats(code):
        # Get statistics about the code.
    lines = code.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    comment_lines = [line for line in lines if line.strip().startswith('//')]
    
    return {
        'total_lines': len(lines),
        'non_empty_lines': len(non_empty_lines),
        'comment_lines': len(comment_lines),
        'code_lines': len(non_empty_lines) - len(comment_lines),
        'characters': len(code)
    }

def format_file_stats(stats):
        # Format file statistics for display.
    return (
        f"{stats['total_lines']} lines "
        f"({stats['code_lines']} code, {stats['comment_lines']} comments), "
        f"{stats['characters']} characters"
    )
