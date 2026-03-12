# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
# No subfunctions - this is a leaf utility function

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": List[Token],   # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }

# === main function ===
def _init_parser_state(tokens: List[Token], filename: str) -> ParserState:
    """
    初始化解析器状态字典。
    
    输入：token 列表和文件名
    输出：ParserState 字典，包含 tokens、pos（初始为 0）、filename 字段
    
    该函数不进行任何验证或处理，仅构建初始状态字典供后续解析使用。
    """
    return {
        "tokens": tokens,
        "pos": 0,
        "filename": filename
    }

# === helper functions ===
# No helper functions needed - logic is trivial

# === OOP compatibility layer ===
# Not needed - this is a utility function, no framework requires class wrapper
