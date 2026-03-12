# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._parse_comparison_package._parse_comparison_src import _parse_comparison

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
def _parse_or_expression(parser_state: ParserState) -> Tuple[AST, ParserState]:
    """
    Parses lowest precedence (or/and) expression.
    Input: parser_state at expression start.
    Output: tuple of (ast_node, updated_parser_state).
    Handles logical operators with lowest precedence and left-associativity.
    """
    # Step 1: Parse left operand using higher precedence parser
    left_ast, state = _parse_comparison(parser_state)
    
    # Step 2: Check if current token is OR or AND keyword
    tokens = state["tokens"]
    pos = state["pos"]
    
    # Step 3: If logical operator found, consume and parse right side
    if pos < len(tokens):
        current_token = tokens[pos]
        if current_token.get("type") == "KEYWORD" and current_token.get("value") in ("or", "and"):
            # Consume the operator token
            op_token = current_token
            state["pos"] = pos + 1
            
            # Step 4: Recursively parse right side (left-associative)
            right_ast, state = _parse_or_expression(state)
            
            # Step 5: Build BINARY_OP AST node
            binary_op_node: AST = {
                "type": "BINARY_OP",
                "value": op_token["value"],
                "children": [left_ast, right_ast],
                "line": op_token.get("line", 0),
                "column": op_token.get("column", 0)
            }
            
            return binary_op_node, state
    
    # Step 6: No logical operator, return left operand as-is
    return left_ast, state

# === helper functions ===
# No helper functions needed - logic is straightforward

# === OOP compatibility layer ===
# Not needed - this is a parser helper function, not a framework entry point
