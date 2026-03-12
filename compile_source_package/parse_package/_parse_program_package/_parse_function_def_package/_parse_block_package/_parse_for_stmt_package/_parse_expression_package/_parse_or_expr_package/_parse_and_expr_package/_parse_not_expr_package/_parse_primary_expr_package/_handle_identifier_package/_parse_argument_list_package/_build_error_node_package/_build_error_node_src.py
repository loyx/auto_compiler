# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this utility function

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
    构建错误 AST 节点，用于报告解析错误。
    
    Args:
        parser_state: 解析器状态字典（会被突变，设置 error 字段）
        message: 错误描述信息
        line: 错误发生的行号
        column: 错误发生的列号
    
    Returns:
        ERROR 类型的 AST 节点字典
    """
    # 创建 ERROR 类型的 AST 节点
    error_node: AST = {
        "type": "ERROR",
        "message": message,
        "line": line,
        "column": column
    }
    
    # 标记解析器状态为错误
    parser_state["error"] = "解析失败"
    
    return error_node

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function