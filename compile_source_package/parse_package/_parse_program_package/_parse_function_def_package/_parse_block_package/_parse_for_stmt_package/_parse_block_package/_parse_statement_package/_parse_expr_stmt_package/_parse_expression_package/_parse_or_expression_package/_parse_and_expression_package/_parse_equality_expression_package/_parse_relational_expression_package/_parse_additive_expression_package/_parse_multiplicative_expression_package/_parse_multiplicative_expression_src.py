# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_expression_package._parse_unary_expression_src import _parse_unary_expression

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
def _parse_multiplicative_expression(parser_state: ParserState) -> AST:
    """
    解析乘法表达式（*、/）。使用左递归消除后的循环结构。
    输入 parser_state（pos 指向表达式起始），返回 AST 节点，原地更新 pos。
    """
    # 1. 先调用 _parse_unary_expression 获取左操作数
    left = _parse_unary_expression(parser_state)
    
    # 2. 当遇到 * 或 / token 时，循环
    while parser_state["pos"] < len(parser_state["tokens"]):
        token = parser_state["tokens"][parser_state["pos"]]
        
        if token["type"] not in ("STAR", "SLASH"):
            break
        
        # 记录运算符位置
        op = token["value"]
        line = token["line"]
        column = token["column"]
        
        # pos 前进
        parser_state["pos"] += 1
        
        # 调用 _parse_unary_expression 获取右操作数
        right = _parse_unary_expression(parser_state)
        
        # 构建 BINARY_OP 节点
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": op,
            "line": line,
            "column": column
        }
    
    # 3. 返回最终的 AST 节点
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function