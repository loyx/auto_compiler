# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_not_package._parse_not_src import _parse_not

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
def _parse_and(parser_state: ParserState) -> AST:
    """解析 and 表达式（比 or 高一优先级的二元运算符）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 解析左操作数（not 表达式）
    left = _parse_not(parser_state)
    
    # 循环处理 AND 运算符（左结合）
    while pos < len(tokens):
        token = tokens[pos]
        if token.get("type") != "AND":
            break
        
        # 记录运算符位置
        op_line = token.get("line", 0)
        op_column = token.get("column", 0)
        
        # 消费 AND token
        parser_state["pos"] = pos + 1
        pos = parser_state["pos"]
        
        # 解析右操作数
        right = _parse_not(parser_state)
        
        # 构建 BINARY_OP AST 节点
        left = {
            "type": "BINARY_OP",
            "operator": "and",
            "children": [left, right],
            "line": op_line,
            "column": op_column
        }
        
        # 更新位置继续循环
        pos = parser_state["pos"]
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node