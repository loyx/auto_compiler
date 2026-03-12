# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_conditional_package._parse_conditional_src import _parse_conditional

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_assignment(parser_state: dict) -> dict:
    """解析赋值表达式：处理 =、+=、-=、*=、/=、%= 等赋值运算符（最低优先级）。"""
    # 步骤 1: 先解析左侧表达式（调用下层解析函数）
    left = _parse_conditional(parser_state)
    
    # 步骤 2: 检查当前 token 是否为赋值运算符
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        # 没有更多 token，直接返回左侧表达式
        return left
    
    current_token = tokens[pos]
    operator = current_token.get("value", "")
    
    # 赋值运算符集合
    assignment_operators = {"=", "+=", "-=", "*=", "/=", "%="}
    
    if operator not in assignment_operators:
        # 不是赋值运算符，返回左侧表达式
        return left
    
    # 步骤 3: 是赋值运算符，记录位置信息
    op_line = current_token.get("line", 0)
    op_column = current_token.get("column", 0)
    
    # 前进 pos（消耗赋值运算符 token）
    parser_state["pos"] += 1
    
    # 步骤 4: 递归解析右侧的赋值表达式（支持连续赋值 a = b = c）
    right = _parse_assignment(parser_state)
    
    # 步骤 5: 返回 ASSIGNMENT 类型的 AST 节点
    return {
        "type": "ASSIGNMENT",
        "operator": operator,
        "left": left,
        "right": right,
        "line": left.get("line", op_line),
        "column": left.get("column", op_column)
    }

# === helper functions ===
# No helper functions needed for this simple parsing logic

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function nodes
