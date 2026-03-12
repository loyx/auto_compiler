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
def _parse_or(parser_state: ParserState) -> AST:
    """
    解析 or 表达式（最低优先级二元运算符）。
    
    处理行为：
    1. 调用 _parse_and 解析左操作数
    2. 循环检查当前 token 是否为 OR 类型
    3. 如果是 OR：记录运算符位置，消费 OR token，调用 _parse_and 解析右操作数
    4. 构建 BINARY_OP AST：{"type": "BINARY_OP", "operator": "or", "children": [left, right], ...}
    5. 继续循环检查下一个 OR token（左结合）
    6. 返回最终的 AST 节点
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 解析左操作数（and 表达式）
    left = _parse_and(parser_state)
    
    # 循环处理 OR 运算符（左结合）
    while pos < len(tokens):
        token = tokens[pos]
        if token.get("type") != "OR":
            break
        
        # 记录 OR 运算符位置
        op_line = token.get("line", 0)
        op_column = token.get("column", 0)
        
        # 消费 OR token
        parser_state["pos"] = pos + 1
        pos = pos + 1
        
        # 解析右操作数（and 表达式）
        right = _parse_and(parser_state)
        
        # 构建 BINARY_OP AST 节点（左结合）
        left = {
            "type": "BINARY_OP",
            "operator": "or",
            "children": [left, right],
            "line": op_line,
            "column": op_column
        }
        
        # 更新位置继续循环
        pos = parser_state["pos"]
    
    return left

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function nodes
