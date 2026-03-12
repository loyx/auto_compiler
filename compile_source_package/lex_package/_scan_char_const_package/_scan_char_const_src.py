# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this implementation

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token type (CHAR_CONST)
#   "value": str,            # token value (original string from source, including quotes)
#   "line": int,             # line number (1-based)
#   "column": int            # column number (1-based)
# }

# === main function ===
def _scan_char_const(source: str, pos: int, line: int, column: int, filename: str) -> tuple:
    """
    Scan a character constant starting at pos (including opening quote).
    
    Returns: tuple (token, new_pos, new_column)
    - token: Token dict with type "CHAR_CONST"
    - new_pos: position after closing quote
    - new_column: column after closing quote
    """
    start_pos = pos
    start_line = line
    start_column = column
    
    # Expect current char is opening quote
    if pos >= len(source) or source[pos] != "'":
        raise Exception(f"{filename}:{line}:{column}: error: expected opening quote")
    
    pos += 1
    column += 1
    
    # Read character content
    if pos >= len(source):
        raise Exception(f"{filename}:{start_line}:{start_column}: error: unterminated character constant")
    
    char = source[pos]
    
    if char == "\\":
        # Handle escape sequence
        pos += 1
        column += 1
        
        if pos >= len(source):
            raise Exception(f"{filename}:{start_line}:{start_column}: error: unterminated character constant")
        
        escape_char = source[pos]
        
        # Validate escape sequence
        valid_escapes = {'n', 't', 'r', '\\', '\'', '"', '0', 'a', 'b', 'v', 'f', '?'}
        if escape_char not in valid_escapes:
            # Still accept it as valid escape, just move past it
            pass
        
        pos += 1
        column += 1
    else:
        # Regular character
        pos += 1
        column += 1
    
    # Expect closing quote
    if pos >= len(source) or source[pos] != "'":
        raise Exception(f"{filename}:{start_line}:{start_column}: error: unterminated character constant")
    
    pos += 1
    column += 1
    
    # Build token
    value = source[start_pos:pos]
    token: Token = {
        "type": "CHAR_CONST",
        "value": value,
        "line": start_line,
        "column": start_column
    }
    
    return (token, pos, column)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
