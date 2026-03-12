# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed - this is a leaf utility function

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
    Build an ERROR AST node and set parser_state error flag.
    
    Resource Write: Mutates parser_state dict (GLOBAL_STATE) by setting error field.
    Side effect: parser_state["error"] = "解析失败"
    Returns: ERROR AST node with message and source location.
    """
    # Set error flag in parser state (GLOBAL_STATE write)
    parser_state["error"] = "解析失败"
    
    # Build and return ERROR node
    return {
        "type": "ERROR",
        "value": message,
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed - logic is minimal

# === OOP compatibility layer ===
# Not needed - this is a utility function, not a framework entry point
