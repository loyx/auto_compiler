# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple utility

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
def _get_current_token(parser_state: ParserState) -> Token:
    """
    获取当前 token。
    
    从 parser_state 中读取 tokens 列表和当前位置 pos，
    返回当前 token 或 None（如果已到达末尾）。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos < len(tokens):
        return tokens[pos]
    else:
        return None

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function