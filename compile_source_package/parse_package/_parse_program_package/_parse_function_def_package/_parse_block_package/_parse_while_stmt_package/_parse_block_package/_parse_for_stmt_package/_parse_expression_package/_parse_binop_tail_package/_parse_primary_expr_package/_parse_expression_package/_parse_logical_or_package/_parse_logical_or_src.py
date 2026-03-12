# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_logical_and_package._parse_logical_and_src import _parse_logical_and

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
#   "operator": str,
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
def _parse_logical_or(parser_state: ParserState) -> AST:
    """Parse logical OR expressions (||) with left-associativity."""
    left = _parse_logical_and(parser_state)
    
    if parser_state.get("error"):
        return left
    
    while _is_current_token_or(parser_state):
        op_token = _get_current_token(parser_state)
        op_line = op_token.get("line", 0)
        op_column = op_token.get("column", 0)
        
        parser_state["pos"] += 1
        
        if _is_at_end(parser_state):
            parser_state["error"] = "Expected operand after ||"
            return _make_error_node("Expected operand after ||", op_line, op_column)
        
        right = _parse_logical_and(parser_state)
        
        if parser_state.get("error"):
            return right
        
        left = _make_binary_op_node("||", left, right, op_line, op_column)
    
    return left

# === helper functions ===
def _is_current_token_or(parser_state: ParserState) -> bool:
    """Check if current token is OR (||)."""
    if _is_at_end(parser_state):
        return False
    token = parser_state["tokens"][parser_state["pos"]]
    return token.get("type") == "OR"

def _get_current_token(parser_state: ParserState) -> Token:
    """Get current token from parser state."""
    return parser_state["tokens"][parser_state["pos"]]

def _is_at_end(parser_state: ParserState) -> bool:
    """Check if parser has reached end of tokens."""
    return parser_state["pos"] >= len(parser_state["tokens"])

def _make_binary_op_node(operator: str, left: AST, right: AST, line: int, column: int) -> AST:
    """Create a BINARY_OP AST node."""
    return {
        "type": "BINARY_OP",
        "operator": operator,
        "children": [left, right],
        "line": line,
        "column": column
    }

def _make_error_node(message: str, line: int, column: int) -> AST:
    """Create an ERROR AST node."""
    return {
        "type": "ERROR",
        "value": message,
        "line": line,
        "column": column
    }

# === OOP compatibility layer ===
