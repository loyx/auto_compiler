# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr

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
def _parse_multiplicative_expr(parser_state: ParserState) -> AST:
    """
    解析乘法表达式（*, /, %）。
    调用原子表达式解析器获取左侧操作数，循环检查后续 token 是否为乘法运算符。
    如果是，消费 token 并解析右侧操作数，构建 BINARY_OP 节点。左结合性。
    """
    # 1. 解析左侧操作数
    left = _parse_primary_expr(parser_state)
    
    # 2. 循环处理乘法运算符
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    while pos < len(tokens):
        token = tokens[pos]
        
        # 检查是否为乘法运算符
        if token["type"] == "OPERATOR" and token["value"] in ["*", "/", "%"]:
            # 消费运算符 token
            parser_state["pos"] = pos + 1
            op_token = token
            
            # 解析右侧操作数
            right = _parse_primary_expr(parser_state)
            
            # 构建 BINARY_OP 节点
            left = {
                "type": "BINARY_OP",
                "operator": op_token["value"],
                "children": [left, right],
                "line": op_token["line"],
                "column": op_token["column"]
            }
            
            # 更新位置
            pos = parser_state["pos"]
        else:
            break
    
    return left


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function