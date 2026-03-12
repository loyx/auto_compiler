# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr

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
def _parse_multiplicative_expr(parser_state: ParserState) -> AST:
    """
    解析乘除法操作符（*、/、%）表达式。
    优先级高于加减操作符但低于一元操作符。
    """
    # 1. 解析左侧操作数（下一优先级）
    left_node = _parse_unary_expr(parser_state)
    
    # 2. 循环检查乘除操作符（左结合）
    while _is_multiplicative_operator(parser_state):
        tokens = parser_state["tokens"]
        pos = parser_state["pos"]
        op_token = tokens[pos]
        
        # 3. 消费操作符 token
        parser_state["pos"] = pos + 1
        operator = op_token["value"]
        line = op_token["line"]
        column = op_token["column"]
        
        # 4. 解析右侧操作数
        right_node = _parse_unary_expr(parser_state)
        
        # 5. 构建 BINARY_OP 节点
        left_node = {
            "type": "BINARY_OP",
            "operator": operator,
            "left": left_node,
            "right": right_node,
            "line": line,
            "column": column
        }
    
    return left_node

# === helper functions ===
def _is_multiplicative_operator(parser_state: ParserState) -> bool:
    """
    检查当前 token 是否为乘除操作符（*、/、%）。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        return False
    
    token = tokens[pos]
    return (
        token.get("type") == "OPERATOR" and
        token.get("value") in ("*", "/", "%")
    )

# === OOP compatibility layer ===
# Not needed for parser function nodes
