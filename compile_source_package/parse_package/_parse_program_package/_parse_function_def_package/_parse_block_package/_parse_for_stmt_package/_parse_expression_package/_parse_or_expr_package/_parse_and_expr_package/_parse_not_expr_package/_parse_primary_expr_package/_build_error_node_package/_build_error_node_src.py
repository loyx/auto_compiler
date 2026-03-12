# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# (none - no delegated child functions)

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
    Build an ERROR type AST node and mark parser state as failed.
    
    Args:
        parser_state: Parser state dictionary to set error flag
        message: Error message string
        line: Line number where error occurred
        column: Column number where error occurred
    
    Returns:
        ERROR AST node with type, value, line, and column fields
    """
    # Set global error flag in parser state
    parser_state["error"] = "解析失败"
    
    # Build and return ERROR node
    error_node: AST = {
        "type": "ERROR",
        "value": message,
        "line": line,
        "column": column
    }
    
    return error_node

# === helper functions ===
# (none needed - logic is simple and self-contained)

# === OOP compatibility layer ===
# (not needed - this is a helper function node, not a framework entry point)
