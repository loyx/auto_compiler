# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_or_expr_package._parse_or_expr_src import _parse_or_expr

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
#   "left": AST,
#   "right": AST,
#   "operand": AST,
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
def _parse_expression(parser_state: dict) -> dict:
    """解析表达式。
    
    Args:
        parser_state: 包含 tokens 列表和 pos 当前位置的字典
        
    Returns:
        AST 节点，类型为 LITERAL、IDENTIFIER、BINARY_OP 或 UNARY_OP
        
    Raises:
        SyntaxError: 当遇到无效表达式时
    """
    # 从最低优先级开始解析（||）
    return _parse_or_expr(parser_state)

# === helper functions ===

# === OOP compatibility layer ===
