# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_arith_expr_package._parse_arith_expr_src import _parse_arith_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (EQ, NE, LT, GT, LE, GE, etc.)
#   "value": str,            # token 值 (==, !=, <, >, <=, >=, etc.)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, ERROR, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值（运算符字符串或标识符/字面量值）
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }

# === main function ===
def _parse_comparison(parser_state: ParserState) -> AST:
    """解析比较表达式。支持左结合链式比较（如 a > b > c）。"""
    # 1. 解析左侧算术表达式
    left = _parse_arith_expr(parser_state)
    
    # 检查是否有错误
    if parser_state.get("error"):
        return left
    
    # 2. 循环解析比较运算符和右侧算术表达式
    comparison_ops = {"EQ", "NE", "LT", "GT", "LE", "GE"}
    
    while True:
        # 检查是否还有 token
        if parser_state["pos"] >= len(parser_state["tokens"]):
            break
        
        current_token = parser_state["tokens"][parser_state["pos"]]
        
        # 检查是否为比较运算符
        if current_token["type"] not in comparison_ops:
            break
        
        # 消费比较运算符 token
        op_token = current_token
        parser_state["pos"] += 1
        
        # 解析右侧算术表达式
        right = _parse_arith_expr(parser_state)
        
        # 检查右侧解析是否失败
        if parser_state.get("error"):
            return right
        
        # 构建 BINARY_OP 节点
        left = {
            "type": "BINARY_OP",
            "value": op_token["value"],
            "children": [left, right],
            "line": left.get("line", op_token["line"]),
            "column": left.get("column", op_token["column"])
        }
    
    return left

# === helper functions ===
def _create_error_node(parser_state: ParserState, message: str) -> AST:
    """创建错误 AST 节点。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    
    # 获取当前位置的行号和列号
    if pos < len(tokens):
        line = tokens[pos]["line"]
        column = tokens[pos]["column"]
    elif len(tokens) > 0:
        # 使用最后一个 token 的位置
        line = tokens[-1]["line"]
        column = tokens[-1]["column"]
    else:
        line = 1
        column = 1
    
    return {
        "type": "ERROR",
        "value": message,
        "children": [],
        "line": line,
        "column": column
    }

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function node.
