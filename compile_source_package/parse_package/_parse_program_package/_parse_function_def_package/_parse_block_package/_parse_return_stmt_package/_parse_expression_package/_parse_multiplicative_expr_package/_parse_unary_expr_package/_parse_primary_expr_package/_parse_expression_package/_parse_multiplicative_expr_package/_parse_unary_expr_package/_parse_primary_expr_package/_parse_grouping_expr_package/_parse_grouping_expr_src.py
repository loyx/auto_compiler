# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression

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
def _parse_grouping_expr(parser_state: ParserState, left_paren: Token) -> AST:
    """
    解析括号表达式：消费左括号，解析内部表达式，期望右括号。
    返回 GROUPING AST 节点。
    """
    # Step 1: Consume LEFT_PAREN (move position forward)
    parser_state["pos"] += 1
    
    # Step 2: Parse inner expression
    inner_expr = _parse_expression(parser_state)
    
    # Step 3: Check for RIGHT_PAREN
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(
            f"Missing ')' in {parser_state['filename']}:"
            f"{left_paren['line']}:{left_paren['column']}"
        )
    
    next_token = tokens[pos]
    if next_token["type"] != "RIGHT_PAREN":
        raise SyntaxError(
            f"Expected ')' but got '{next_token['value']}' in "
            f"{parser_state['filename']}:{next_token['line']}:{next_token['column']}"
        )
    
    # Step 4: Consume RIGHT_PAREN
    parser_state["pos"] += 1
    
    # Step 5: Return GROUPING AST node
    return {
        "type": "GROUPING",
        "children": [inner_expr],
        "value": None,
        "line": left_paren["line"],
        "column": left_paren["column"]
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node
