# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No child functions needed for this utility function

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
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }

# === main function ===
def _current_token(parser_state: ParserState) -> Optional[Token]:
    """
    获取解析器状态中当前位置的 token。
    
    Args:
        parser_state: 解析器状态字典，包含 tokens、pos、filename 等字段
        
    Returns:
        当前位置的 Token 字典，如果越界则返回 None
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 如果 tokens 为 None，直接返回 None
    if tokens is None:
        return None
    
    # 检查 pos 是否在 tokens 列表范围内
    if 0 <= pos < len(tokens):
        return tokens[pos]
    else:
        return None

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed for this utility function