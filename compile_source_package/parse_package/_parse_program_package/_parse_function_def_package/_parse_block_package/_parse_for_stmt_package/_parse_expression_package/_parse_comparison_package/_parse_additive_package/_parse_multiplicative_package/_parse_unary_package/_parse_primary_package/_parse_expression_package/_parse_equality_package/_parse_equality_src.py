# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_package._parse_comparison_src import _parse_comparison

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
#   "column": int,
#   "operator": str,
#   "left": dict,
#   "right": dict
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
def _parse_equality(parser_state: dict) -> dict:
    """
    解析 equality 层级表达式 (== 和 != 运算符)。
    语法：equality := comparison ( ( "==" | "!=" ) comparison )*
    """
    # 解析左侧 comparison
    left_ast = _parse_comparison(parser_state)
    
    # 检查是否有错误
    if parser_state.get("error"):
        return left_ast
    
    # 循环处理 equality 运算符
    while True:
        if parser_state["pos"] >= len(parser_state["tokens"]):
            break
        
        current_token = parser_state["tokens"][parser_state["pos"]]
        
        # 检查是否为 equality 运算符
        if current_token.get("type") != "OPERATOR" or current_token.get("value") not in ("==", "!="):
            break
        
        # 记录运算符和位置信息
        operator = current_token["value"]
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        
        # 前进 pos
        parser_state["pos"] += 1
        
        # 解析右侧 comparison
        right_ast = _parse_comparison(parser_state)
        
        # 检查是否有错误
        if parser_state.get("error"):
            return left_ast
        
        # 构建 Binary AST 节点
        left_ast = {
            "type": "Binary",
            "operator": operator,
            "left": left_ast,
            "right": right_ast,
            "line": line,
            "column": column
        }
    
    return left_ast

# === helper functions ===
# No helper functions needed - all logic is in main function

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node