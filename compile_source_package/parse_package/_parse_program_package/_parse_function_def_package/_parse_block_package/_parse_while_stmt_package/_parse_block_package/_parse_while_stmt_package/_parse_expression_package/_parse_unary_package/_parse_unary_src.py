# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._parse_power_package._parse_power_src import _parse_power
from ._peek_token_package._peek_token_src import _peek_token
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
def _parse_unary(parser_state: ParserState) -> Tuple[AST, ParserState]:
    """
    解析一元表达式（-, +, not）。
    支持连续一元运算符（如 --x）。
    """
    current_token = _peek_token(parser_state)
    
    if current_token is None:
        return _parse_power(parser_state)
    
    token_type = current_token.get("type", "")
    token_line = current_token.get("line", 0)
    token_column = current_token.get("column", 0)
    
    operator_map = {
        "MINUS": "-",
        "PLUS": "+",
        "NOT": "not"
    }
    
    if token_type in operator_map:
        op = operator_map[token_type]
        _, parser_state = _consume_token(parser_state)
        
        operand_ast, parser_state = _parse_unary(parser_state)
        
        ast_node = {
            "type": "UNARY_OP",
            "operator": op,
            "children": [operand_ast],
            "line": token_line,
            "column": token_column
        }
        
        return ast_node, parser_state
    else:
        return _parse_power(parser_state)

# === helper functions ===
# No helper functions needed; main logic is self-contained

# === OOP compatibility layer ===
# No OOP wrapper needed for parser utility function
