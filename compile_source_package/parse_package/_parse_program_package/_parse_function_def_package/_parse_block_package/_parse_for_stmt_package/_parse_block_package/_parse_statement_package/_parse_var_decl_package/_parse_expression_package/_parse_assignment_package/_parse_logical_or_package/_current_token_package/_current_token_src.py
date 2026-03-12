# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple accessor

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
def _current_token(parser_state: ParserState) -> Token:
    """
    获取解析器状态中的当前 token。
    
    Args:
        parser_state: 解析器状态字典，包含 tokens、pos、filename 等字段
        
    Returns:
        当前 token 字典，如果已超出 tokens 范围则返回 None
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 检查 pos 是否在有效范围内
    if pos < 0 or pos >= len(tokens):
        return None
    
    return tokens[pos]

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function
