# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_package._parse_multiplicative_src import _parse_multiplicative

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
def _parse_additive(parser_state: ParserState) -> AST:
    """
    解析加减表达式。使用左递归消除后的循环结构。
    
    1. 先调用 _parse_multiplicative 获取左操作数
    2. 当遇到 + 或 - token 时，循环构建 BINARY_OP 节点
    3. 返回最终的 AST 节点
    """
    # 获取左操作数
    left = _parse_multiplicative(parser_state)
    
    # 循环处理 + 和 - 运算符
    while parser_state["pos"] < len(parser_state["tokens"]):
        token = parser_state["tokens"][parser_state["pos"]]
        
        # 检查是否为加减运算符
        if token["type"] not in ("PLUS", "MINUS"):
            break
        
        # 记录运算符信息
        op_token = token
        parser_state["pos"] += 1
        
        # 获取右操作数
        right = _parse_multiplicative(parser_state)
        
        # 构建 BINARY_OP 节点
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": op_token["value"],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function