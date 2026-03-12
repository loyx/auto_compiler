# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._peek_token_package._peek_token_src import _peek_token
from ._consume_token_package._consume_token_src import _consume_token
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
def _parse_unary(parser_state: ParserState) -> tuple:
    """
    解析一元表达式（+x, -x, ~x, not x 等）。
    返回 (AST 节点，更新后的 parser_state)。
    """
    UNARY_OPERATORS = {"PLUS", "MINUS", "TILDE", "NOT"}
    
    current_token = _peek_token(parser_state)
    
    if current_token is None:
        return _parse_primary(parser_state)
    
    token_type = current_token.get("type", "")
    
    if token_type in UNARY_OPERATORS:
        op_token = _consume_token(parser_state)
        op_value = op_token.get("value", "")
        line = op_token.get("line", 0)
        column = op_token.get("column", 0)
        
        operand_ast, updated_state = _parse_unary(parser_state)
        
        unary_node = {
            "type": "UNARY_OP",
            "operator": op_value,
            "children": [operand_ast],
            "line": line,
            "column": column
        }
        
        return (unary_node, updated_state)
    else:
        return _parse_primary(parser_state)

# === helper functions ===
# No helper functions needed; all logic is in main function.

# === OOP compatibility layer ===
# Not needed for this parser function node.
