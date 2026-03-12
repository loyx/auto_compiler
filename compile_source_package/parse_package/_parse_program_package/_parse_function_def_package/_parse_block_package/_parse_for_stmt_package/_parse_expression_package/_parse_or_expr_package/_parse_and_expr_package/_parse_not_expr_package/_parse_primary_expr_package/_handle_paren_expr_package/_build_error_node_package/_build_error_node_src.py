# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (大写字符串)
#   "value": str,            # token 值 (原始字符串)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (IDENTIFIER, LITERAL, CALL, ERROR, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
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
def _build_error_node(parser_state: ParserState, message: str, line: int, column: int) -> AST:
    """
    Build an ERROR type AST node.
    
    Input: parser_state (parser state dict), message (error message), 
           line (line number), column (column number).
    Output: ERROR node dictionary.
    Side effect: Sets parser_state['error'] = '解析失败'.
    """
    parser_state["error"] = "解析失败"
    
    error_node: AST = {
        "type": "ERROR",
        "value": message,
        "line": line,
        "column": column,
        "children": []
    }
    
    return error_node

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function
