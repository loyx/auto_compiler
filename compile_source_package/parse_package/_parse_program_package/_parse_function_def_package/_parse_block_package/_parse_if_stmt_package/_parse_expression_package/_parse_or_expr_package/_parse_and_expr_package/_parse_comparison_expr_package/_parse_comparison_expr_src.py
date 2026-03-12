# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_expr_package._parse_additive_expr_src import _parse_additive_expr

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
def _parse_comparison_expr(parser_state: ParserState) -> AST:
    """
    解析比较操作符（<, >, <=, >=, ==, !=）。
    优先级高于 && 但低于算术操作符。
    """
    tokens = parser_state["tokens"]
    
    # 解析左侧操作数（下一优先级）
    left_node = _parse_additive_expr(parser_state)
    
    # 比较操作符集合
    comparison_ops = {"<", ">", "<=", ">=", "==", "!="}
    
    # 循环检查比较操作符（左结合）
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        # 检查是否为比较操作符
        if current_token.get("type") != "OPERATOR" or current_token.get("value") not in comparison_ops:
            break
        
        # 消费操作符 token
        op = current_token["value"]
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        parser_state["pos"] += 1
        
        # 解析右侧操作数
        right_node = _parse_additive_expr(parser_state)
        
        # 构建 BINARY_OP 节点
        left_node = {
            "type": "BINARY_OP",
            "operator": op,
            "left": left_node,
            "right": right_node,
            "line": line,
            "column": column
        }
    
    return left_node

# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# Not needed for parser function nodes