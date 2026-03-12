# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions - inline implementation

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
    """
    Parse an expression from the token stream.
    
    Handles: identifiers, literals, binary operations, parenthesized expressions.
    Updates parser_state["pos"] to consume tokens.
    Raises SyntaxError on invalid expression syntax.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Incomplete expression")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    # Handle parenthesized expression
    if token_type == "LPAREN":
        parser_state["pos"] += 1  # consume '('
        left_ast = _parse_expression(parser_state)
        
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError("Incomplete expression")
        
        close_token = tokens[parser_state["pos"]]
        if close_token["type"] != "RPAREN":
            raise SyntaxError("Expected ')'")
        
        parser_state["pos"] += 1  # consume ')'
        return left_ast
    
    # Handle literals and identifiers
    elif token_type in ("NUMBER", "STRING", "IDENTIFIER"):
        ast_node = {
            "type": token_type,
            "value": current_token["value"],
            "line": current_token["line"],
            "column": current_token["column"]
        }
        parser_state["pos"] += 1  # consume token
        
        # Check for binary operator
        if _is_operator_at(parser_state):
            return _parse_binary_op(parser_state, ast_node)
        
        return ast_node
    
    else:
        raise SyntaxError("Invalid expression start")

# === helper functions ===
def _is_operator_at(parser_state: ParserState) -> bool:
    """Check if current position has a binary operator token."""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    
    if pos >= len(tokens):
        return False
    
    operator_types = {"PLUS", "MINUS", "MULTIPLY", "DIVIDE", "EQUALS", "LESS", "GREATER"}
    return tokens[pos]["type"] in operator_types

def _parse_binary_op(parser_state: ParserState, left_ast: AST) -> AST:
    """
    Parse binary operation: left_expr OPERATOR right_expr.
    
    Assumes left_ast is already parsed and pos is at operator token.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    operator_token = tokens[pos]
    operator = operator_token["value"]
    line = operator_token["line"]
    column = operator_token["column"]
    
    parser_state["pos"] += 1  # consume operator
    
    # Parse right expression
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError("Incomplete expression")
    
    right_ast = _parse_expression(parser_state)
    
    return {
        "type": "BINARY_OP",
        "operator": operator,
        "line": line,
        "column": column,
        "children": [left_ast, right_ast]
    }

# === OOP compatibility layer ===
# Not needed - this is a helper parser function, not a framework entry point
