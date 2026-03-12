# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
from ._parse_let_stmt_package._parse_let_stmt_src import _parse_let_stmt

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "line": int,
#   "column": int
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_block(parser_state: ParserState) -> AST:
    """Parse a statement block until SEMICOLON."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    statements = []
    first_line = None
    first_column = None
    
    while pos < len(tokens):
        token = tokens[pos]
        
        if token["type"] == "SEMICOLON":
            break
        
        if token["type"] == "WHILE":
            if first_line is None:
                first_line = token["line"]
                first_column = token["column"]
            stmt_ast = _parse_while_stmt(parser_state)
            statements.append(stmt_ast)
            pos = parser_state["pos"]
        elif token["type"] == "LET":
            if first_line is None:
                first_line = token["line"]
                first_column = token["column"]
            stmt_ast = _parse_let_stmt(parser_state)
            statements.append(stmt_ast)
            pos = parser_state["pos"]
        else:
            raise SyntaxError(
                f"Expected statement (WHILE or LET) at {filename}:"
                f"{token['line']}:{token['column']}"
            )
    
    if pos >= len(tokens):
        raise SyntaxError(
            f"Expected SEMICOLON at end of block at {filename}:EOF"
        )
    
    if first_line is None:
        colon_pos = pos - 1
        if colon_pos >= 0:
            first_line = tokens[colon_pos]["line"]
            first_column = tokens[colon_pos]["column"]
        else:
            first_line = 0
            first_column = 0
    
    parser_state["pos"] = pos
    
    return {
        "type": "BODY",
        "line": first_line,
        "column": first_column,
        "children": statements
    }

# === helper functions ===

# === OOP compatibility layer ===
