# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._parse_additive_package._parse_additive_src import _parse_additive
from ._consume_token_package._consume_token_src import _consume_token

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
def _parse_comparison(parser_state: ParserState) -> Tuple[AST, ParserState]:
    """
    解析比较表达式（==, !=, <, >, <=, >=）。
    这是表达式优先级链中位于 _parse_and 之下的层级。
    """
    # Step 1: Parse left operand (additive expression)
    left_ast, parser_state = _parse_additive(parser_state)
    
    # Step 2: Check if current token is a comparison operator
    comparison_ops = {"==", "!=", "<", ">", "<=", ">="}
    
    if parser_state["pos"] >= len(parser_state["tokens"]):
        # No more tokens, return left operand as-is
        return left_ast, parser_state
    
    current_token = parser_state["tokens"][parser_state["pos"]]
    
    if current_token["value"] not in comparison_ops:
        # Not a comparison operator, return left operand as-is
        return left_ast, parser_state
    
    # Step 3: Consume the comparison operator token
    op_token, parser_state = _consume_token(parser_state, current_token["type"])
    
    # Step 4: Parse right operand (additive expression)
    right_ast, parser_state = _parse_additive(parser_state)
    
    # Step 5: Build BINARY_OP AST node
    binary_op_node: AST = {
        "type": "BINARY_OP",
        "value": op_token["value"],
        "children": [left_ast, right_ast],
        "line": op_token["line"],
        "column": op_token["column"]
    }
    
    return binary_op_node, parser_state

# === helper functions ===
# No helper functions needed - all logic is in main function

# === OOP compatibility layer ===
# Not needed for parser function nodes
