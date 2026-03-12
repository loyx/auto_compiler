# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary

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
def _parse_expression(parser_state: ParserState) -> AST:
    """Parse a complete expression with all operator precedence levels."""
    return _parse_or(parser_state)

# === helper functions ===
def _parse_or(parser_state: ParserState) -> AST:
    """Parse OR expressions (lowest precedence)."""
    return _parse_binary_left_assoc(parser_state, ["OR"], _parse_and)

def _parse_and(parser_state: ParserState) -> AST:
    """Parse AND expressions."""
    return _parse_binary_left_assoc(parser_state, ["AND"], _parse_equality)

def _parse_equality(parser_state: ParserState) -> AST:
    """Parse equality expressions (==, !=)."""
    return _parse_binary_left_assoc(parser_state, ["EQ", "NE"], _parse_comparison)

def _parse_comparison(parser_state: ParserState) -> AST:
    """Parse comparison expressions (<, >, <=, >=)."""
    return _parse_binary_left_assoc(parser_state, ["LT", "GT", "LE", "GE"], _parse_additive)

def _parse_additive(parser_state: ParserState) -> AST:
    """Parse additive expressions (+, -)."""
    return _parse_binary_left_assoc(parser_state, ["PLUS", "MINUS"], _parse_multiplicative)

def _parse_multiplicative(parser_state: ParserState) -> AST:
    """Parse multiplicative expressions (*, /)."""
    return _parse_binary_left_assoc(parser_state, ["MUL", "DIV"], _parse_unary)

def _parse_unary(parser_state: ParserState) -> AST:
    """Parse unary expressions (-, NOT)."""
    if _check_token_types(parser_state, ["MINUS", "NOT"]):
        op = _consume_token(parser_state)
        operand = _parse_unary(parser_state)
        return _build_unary_op(op, operand)
    return _parse_primary(parser_state)

def _parse_binary_left_assoc(parser_state: ParserState, op_types: list, next_parser) -> AST:
    """Parse left-associative binary expressions."""
    left = next_parser(parser_state)
    while _check_token_types(parser_state, op_types):
        op = _consume_token(parser_state)
        right = next_parser(parser_state)
        left = _build_binary_op(op, left, right)
    return left

def _check_token_types(parser_state: ParserState, types: list) -> bool:
    """Check if current token matches any of the given types."""
    if parser_state["pos"] >= len(parser_state["tokens"]):
        return False
    return parser_state["tokens"][parser_state["pos"]]["type"] in types

def _consume_token(parser_state: ParserState) -> Token:
    """Consume and return the current token."""
    if parser_state["pos"] >= len(parser_state["tokens"]):
        _raise_error(parser_state, "Unexpected end of expression")
    token = parser_state["tokens"][parser_state["pos"]]
    parser_state["pos"] += 1
    return token

def _build_binary_op(op: Token, left: AST, right: AST) -> AST:
    """Build a binary operator AST node."""
    return {
        "type": "BINARY_OP",
        "value": {"operator": op["value"]},
        "children": [left, right],
        "line": op["line"],
        "column": op["column"]
    }

def _build_unary_op(op: Token, operand: AST) -> AST:
    """Build a unary operator AST node."""
    return {
        "type": "UNARY_OP",
        "value": {"operator": op["value"]},
        "children": [operand],
        "line": op["line"],
        "column": op["column"]
    }

def _raise_error(parser_state: ParserState, message: str) -> None:
    """Raise a syntax error with proper location info."""
    pos = min(parser_state["pos"], len(parser_state["tokens"]) - 1)
    if parser_state["tokens"]:
        token = parser_state["tokens"][pos]
        line, col = token["line"], token["column"]
    else:
        line, col = 1, 1
    raise SyntaxError(f"{parser_state['filename']}:{line}:{col}: {message}")