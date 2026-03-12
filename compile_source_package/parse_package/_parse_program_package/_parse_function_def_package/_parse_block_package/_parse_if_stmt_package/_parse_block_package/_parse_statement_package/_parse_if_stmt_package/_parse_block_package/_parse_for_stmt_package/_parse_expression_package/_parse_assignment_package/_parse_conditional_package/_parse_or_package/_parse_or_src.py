# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_package._parse_and_src import _parse_and

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
#   "left": Any,
#   "right": Any,
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
def _parse_or(parser_state: ParserState) -> ParserState:
    """
    解析逻辑或运算符表达式（||）。
    优先级低于条件运算符但高于逻辑与运算符。
    支持左结合：a || b || c 解析为 (a || b) || c
    """
    # 步骤 1: 调用下层解析函数获取左操作数
    left_ast = _parse_and(parser_state)
    
    # 步骤 2: 循环检查当前 token 是否为 ||
    while True:
        tokens = parser_state["tokens"]
        pos = parser_state["pos"]
        
        # 检查是否还有 token
        if pos >= len(tokens):
            break
        
        current_token = tokens[pos]
        
        # 检查是否为 || 运算符
        if current_token.get("value") != "||":
            break
        
        # 步骤 3: 是 ||，消耗该 token
        or_line = current_token.get("line", 0)
        or_column = current_token.get("column", 0)
        parser_state["pos"] = pos + 1
        
        # 调用下层解析函数获取右操作数
        right_ast = _parse_and(parser_state)
        
        # 构建 OR 类型 AST 节点
        left_ast = {
            "type": "OR",
            "left": left_ast,
            "right": right_ast,
            "line": or_line,
            "column": or_column
        }
    
    return left_ast

# === helper functions ===
# No helper functions needed for this simple parsing logic

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function nodes
