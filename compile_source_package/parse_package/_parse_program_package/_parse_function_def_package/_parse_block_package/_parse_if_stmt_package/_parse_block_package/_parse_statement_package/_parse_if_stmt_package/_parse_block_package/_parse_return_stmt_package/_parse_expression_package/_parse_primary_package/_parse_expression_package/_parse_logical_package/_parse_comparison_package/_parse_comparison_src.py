# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_package._parse_additive_src import _parse_additive

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
def _parse_comparison(parser_state: ParserState) -> AST:
    """
    解析比较表达式（==, !=, <, >, <=, >=）。
    首先调用 _parse_additive 解析左侧操作数，然后检查比较运算符。
    不支持链式比较。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 解析左侧操作数（加法表达式）
    left_ast = _parse_additive(parser_state)
    
    # 检查当前位置是否有比较运算符
    if parser_state["pos"] >= len(tokens):
        return left_ast
    
    current_token = tokens[parser_state["pos"]]
    op = current_token["value"]
    
    comparison_ops = ["==", "!=", "<", ">", "<=", ">="]
    
    if op not in comparison_ops:
        return left_ast
    
    # 记录运算符位置
    op_line = current_token.get("line", 0)
    op_column = current_token.get("column", 0)
    
    # 消耗运算符 token
    parser_state["pos"] += 1
    
    # 解析右侧操作数（加法表达式）
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError(f"{filename}:{op_line}:{op_column}: 比较运算符右侧缺少表达式")
    
    right_ast = _parse_additive(parser_state)
    
    # 构建 BinaryOp AST 节点
    result = {
        "type": "BinaryOp",
        "op": op,
        "left": left_ast,
        "right": right_ast,
        "line": op_line,
        "column": op_column
    }
    
    return result

# === helper functions ===

# === OOP compatibility layer ===
