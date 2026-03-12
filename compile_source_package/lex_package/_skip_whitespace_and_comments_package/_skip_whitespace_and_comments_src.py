# === std / third-party imports ===
from typing import Tuple

# === sub function imports ===
# No sub functions needed

# === ADT defines ===
# No special ADT needed, uses primitive types
# Input: source (str), pos (int), line (int), column (int)
# Output: Tuple[int, int, int] representing (new_pos, new_line, new_column)

# === main function ===
def _skip_whitespace_and_comments(source: str, pos: int, line: int, column: int) -> Tuple[int, int, int]:
    """Skip whitespace and single-line comments in C source code.
    
    Skips spaces, tabs, newlines, carriage returns, and // comments.
    Updates line and column tracking accordingly.
    """
    n = len(source)
    
    while pos < n:
        char = source[pos]
        
        # Skip space
        if char == ' ':
            pos += 1
            column += 1
            continue
        
        # Skip tab
        if char == '\t':
            pos += 1
            column += 1
            continue
        
        # Skip newline
        if char == '\n':
            pos += 1
            line += 1
            column = 1
            continue
        
        # Skip carriage return
        if char == '\r':
            pos += 1
            continue
        
        # Check for single-line comment //
        if char == '/' and pos + 1 < n and source[pos + 1] == '/':
            pos += 2
            column += 2
            while pos < n and source[pos] != '\n':
                pos += 1
                column += 1
            continue
        
        # No more whitespace or comments to skip
        break
    
    return (pos, line, column)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
