# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
# No sub function imports needed - all logic inlined

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token type (KEYWORD_*, IDENTIFIER, INT_CONST, CHAR_CONST, OP_*, SEP_*)
#   "value": str,            # token value (original string from source)
#   "line": int,             # line number (1-based)
#   "column": int            # column number (1-based)
# }

# === main function ===
def lex(source: str, filename: str) -> List[Token]:
    """Lexical analyzer: convert C source code string to token list."""
    tokens: List[Token] = []
    pos: int = 0
    line: int = 1
    column: int = 1
    length: int = len(source)
    
    KEYWORDS = {
        'int', 'char', 'void', 'if', 'else', 'while', 'for', 'return',
        'break', 'continue', 'struct', 'sizeof'
    }
    
    while pos < length:
        # Skip whitespace and comments
        while pos < length:
            char = source[pos]
            if char == ' ':
                pos += 1
                column += 1
            elif char == '\t':
                pos += 1
                column += 1
            elif char == '\n':
                pos += 1
                line += 1
                column = 1
            elif char == '\r':
                pos += 1
            elif char == '/' and pos + 1 < length and source[pos + 1] == '/':
                pos += 2
                column += 2
                while pos < length and source[pos] != '\n':
                    pos += 1
                    column += 1
            else:
                break
        
        if pos >= length:
            break
        
        char = source[pos]
        start_line = line
        start_col = column
        
        # Scan identifier or keyword
        if char.isalpha() or char == '_':
            start_pos = pos
            while pos < length and (source[pos].isalnum() or source[pos] == '_'):
                pos += 1
                column += 1
            value = source[start_pos:pos]
            if value in KEYWORDS:
                token_type = f"KEYWORD_{value.upper()}"
            else:
                token_type = "IDENTIFIER"
            token: Token = {"type": token_type, "value": value, "line": start_line, "column": start_col}
            tokens.append(token)
        # Scan number
        elif char.isdigit():
            start_pos = pos
            while pos < length and source[pos].isdigit():
                pos += 1
                column += 1
            value = source[start_pos:pos]
            token: Token = {"type": "INT_CONST", "value": value, "line": start_line, "column": start_col}
            tokens.append(token)
        # Scan char constant
        elif char == "'":
            start_pos = pos
            pos += 1
            column += 1
            if pos < length and source[pos] == '\\':
                pos += 1
                column += 1
                if pos < length:
                    pos += 1
                    column += 1
            elif pos < length and source[pos] != "'":
                pos += 1
                column += 1
            if pos < length and source[pos] == "'":
                pos += 1
                column += 1
            value = source[start_pos:pos]
            token: Token = {"type": "CHAR_CONST", "value": value, "line": start_line, "column": start_col}
            tokens.append(token)
        # Scan operator or punctuation
        elif char in '+-*/%<>=!&|;(),{}':
            next_char = source[pos + 1] if pos + 1 < length else ''
            two_char = char + next_char
            two_char_ops = {'==', '!=', '<=', '>=', '&&', '||'}
            if two_char in two_char_ops:
                value = two_char
                pos += 2
                column += 2
            else:
                value = char
                pos += 1
                column += 1
            punctuation_set = {';', '(', ')', ',', '{', '}'}
            if value in punctuation_set:
                token_type = f"SEP_{value}"
            else:
                token_type = f"OP_{value}"
            token: Token = {"type": token_type, "value": value, "line": start_line, "column": start_col}
            tokens.append(token)
        # Illegal character
        else:
            raise Exception(f"{filename}:{start_line}:{start_col}: error: unexpected character '{char}'")
    
    return tokens

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this lexical analyzer function
