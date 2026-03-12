# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions needed for this scanner

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token type (OP_*, SEP_*)
#   "value": str,            # token value (original string from source)
#   "line": int,             # line number (1-based)
#   "column": int            # column number (1-based)
# }

ScanResult = Tuple[Token, int, int]
# ScanResult possible fields:
# {
#   "token": Token,          # the scanned token
#   "new_pos": int,          # position after scanning
#   "new_column": int        # column after scanning
# }

# === main function ===
def _scan_operator_or_punctuation(source: str, pos: int, line: int, column: int, filename: str) -> ScanResult:
    """
    Scan an operator or punctuation symbol starting at pos.
    Uses maximal munch to match multi-char operators first.
    Returns tuple (token, new_pos, new_column).
    """
    if pos >= len(source):
        raise ValueError(f"Unexpected end of file at {filename}:{line}:{column}")
    
    current_char = source[pos]
    next_char = source[pos + 1] if pos + 1 < len(source) else None
    
    # Multi-character operators (maximal munch)
    if current_char == '=' and next_char == '=':
        token = _make_token("OP_EQ", "==", line, column)
        return (token, pos + 2, column + 2)
    elif current_char == '!' and next_char == '=':
        token = _make_token("OP_NE", "!=", line, column)
        return (token, pos + 2, column + 2)
    elif current_char == '<' and next_char == '=':
        token = _make_token("OP_LE", "<=", line, column)
        return (token, pos + 2, column + 2)
    elif current_char == '>' and next_char == '=':
        token = _make_token("OP_GE", ">=", line, column)
        return (token, pos + 2, column + 2)
    elif current_char == '&' and next_char == '&':
        token = _make_token("OP_AND", "&&", line, column)
        return (token, pos + 2, column + 2)
    elif current_char == '|' and next_char == '|':
        token = _make_token("OP_OR", "||", line, column)
        return (token, pos + 2, column + 2)
    
    # Single-character operators
    elif current_char == '+':
        token = _make_token("OP_PLUS", "+", line, column)
        return (token, pos + 1, column + 1)
    elif current_char == '-':
        token = _make_token("OP_MINUS", "-", line, column)
        return (token, pos + 1, column + 1)
    elif current_char == '*':
        token = _make_token("OP_MUL", "*", line, column)
        return (token, pos + 1, column + 1)
    elif current_char == '/':
        token = _make_token("OP_DIV", "/", line, column)
        return (token, pos + 1, column + 1)
    elif current_char == '%':
        token = _make_token("OP_MOD", "%", line, column)
        return (token, pos + 1, column + 1)
    elif current_char == '=':
        token = _make_token("OP_ASSIGN", "=", line, column)
        return (token, pos + 1, column + 1)
    elif current_char == '<':
        token = _make_token("OP_LT", "<", line, column)
        return (token, pos + 1, column + 1)
    elif current_char == '>':
        token = _make_token("OP_GT", ">", line, column)
        return (token, pos + 1, column + 1)
    elif current_char == '!':
        token = _make_token("OP_NOT", "!", line, column)
        return (token, pos + 1, column + 1)
    
    # Punctuation symbols
    elif current_char == ';':
        token = _make_token("SEP_SEMICOLON", ";", line, column)
        return (token, pos + 1, column + 1)
    elif current_char == ',':
        token = _make_token("SEP_COMMA", ",", line, column)
        return (token, pos + 1, column + 1)
    elif current_char == '(':
        token = _make_token("SEP_LPAREN", "(", line, column)
        return (token, pos + 1, column + 1)
    elif current_char == ')':
        token = _make_token("SEP_RPAREN", ")", line, column)
        return (token, pos + 1, column + 1)
    elif current_char == '{':
        token = _make_token("SEP_LBRACE", "{", line, column)
        return (token, pos + 1, column + 1)
    elif current_char == '}':
        token = _make_token("SEP_RBRACE", "}", line, column)
        return (token, pos + 1, column + 1)
    
    else:
        raise ValueError(f"Unexpected character '{current_char}' at {filename}:{line}:{column}")

# === helper functions ===
def _make_token(token_type: str, value: str, line: int, column: int) -> Token:
    """Create a token dictionary with the given type, value, and position."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }

# === OOP compatibility layer ===
# Not needed: this is a helper scanner function, not a framework entry point
