# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,         # Token type: INTEGER, FLOAT, STRING, BOOLEAN, NIL, IDENTIFIER, etc.
#   "value": str,        # Token value as string
#   "line": int,         # Line number in source
#   "column": int        # Column number in source
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,         # Node type: VALUE, IDENTIFIER, ERROR, BINARY, etc.
#   "children": list,    # Child AST nodes
#   "value": Any,        # Literal value for VALUE nodes
#   "operator": str,     # Operator for BINARY nodes
#   "operand": Any,      # Operand for unary operations
#   "name": str,         # Identifier name for IDENTIFIER nodes
#   "message": str,      # Error message for ERROR nodes
#   "line": int,         # Line number
#   "column": int        # Column number
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,      # List of Token objects
#   "pos": int,          # Current position in token list (mutable)
#   "filename": str,     # Source filename
#   "error": str         # Error message (mutable, set on failure)
# }


# === main function ===
def _parse_primary(parser_state: ParserState) -> AST:
    """
    解析初级表达式（原子表达式）。
    处理字面量、标识符、括号表达式。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # Check if we have tokens remaining
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return _make_error_node("Unexpected end of input", parser_state)
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    token_value = current_token.get("value", "")
    token_line = current_token.get("line", 0)
    token_column = current_token.get("column", 0)
    
    # Handle literal types
    if token_type in ("INTEGER", "FLOAT", "STRING", "BOOLEAN", "NIL"):
        parser_state["pos"] = pos + 1
        return _make_value_node(token_type, token_value, token_line, token_column)
    
    # Handle identifier
    elif token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return _make_identifier_node(token_value, token_line, token_column)
    
    # Handle parenthesized expression
    elif token_type == "LEFT_PAREN":
        parser_state["pos"] = pos + 1  # consume LEFT_PAREN
        expr_ast = _parse_expression(parser_state)
        
        # Check for error from nested parsing
        if parser_state.get("error"):
            return expr_ast
        
        # Expect RIGHT_PAREN
        new_pos = parser_state.get("pos", 0)
        if new_pos >= len(tokens):
            parser_state["error"] = "Missing closing parenthesis"
            return _make_error_node("Missing closing parenthesis", parser_state)
        
        next_token = tokens[new_pos]
        if next_token.get("type") != "RIGHT_PAREN":
            parser_state["error"] = f"Expected RIGHT_PAREN, got {next_token.get('type')}"
            return _make_error_node(f"Expected RIGHT_PAREN, got {next_token.get('type')}", parser_state)
        
        parser_state["pos"] = new_pos + 1  # consume RIGHT_PAREN
        return expr_ast
    
    # Unknown token type for primary expression
    else:
        parser_state["error"] = f"Unexpected token: {token_type}"
        return _make_error_node(f"Unexpected token: {token_type}", parser_state)


# === helper functions ===
def _make_value_node(token_type: str, value: str, line: int, column: int) -> AST:
    """Create a VALUE AST node for literals."""
    return {
        "type": "VALUE",
        "value": value,
        "value_type": token_type,
        "line": line,
        "column": column
    }


def _make_identifier_node(name: str, line: int, column: int) -> AST:
    """Create an IDENTIFIER AST node."""
    return {
        "type": "IDENTIFIER",
        "name": name,
        "line": line,
        "column": column
    }


def _make_error_node(message: str, parser_state: ParserState) -> AST:
    """Create an ERROR AST node."""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    line = 0
    column = 0
    if pos < len(tokens):
        line = tokens[pos].get("line", 0)
        column = tokens[pos].get("column", 0)
    
    return {
        "type": "ERROR",
        "message": message,
        "line": line,
        "column": column
    }


# === OOP compatibility layer ===
# Not needed for this helper function node
