# === std / third-party imports ===
from typing import Any, Dict, Optional

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
def _current_token(parser_state: ParserState) -> Optional[Token]:
    """获取当前位置的 token。
    
    从 parser_state 中读取 tokens 列表和 pos 位置，
    返回当前位置的 token 字典，若超出范围则返回 None（表示 EOF）。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos < 0 or pos >= len(tokens):
        return None
    
    return tokens[pos]

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
