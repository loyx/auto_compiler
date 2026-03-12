# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions required for this utility function

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
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
def _consume_token(parser_state: ParserState) -> ParserState:
    """
    消费当前 token 并前进位置指针。
    
    从 parser_state 中获取 tokens 列表和 pos 位置指针。
    如果 pos >= len(tokens)，返回原 parser_state（已到达末尾）。
    否则创建 parser_state 的副本，将 pos 加 1。
    不修改原始 parser_state（函数式风格）。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 如果已到达 tokens 末尾，返回原状态
    if pos >= len(tokens):
        return parser_state
    
    # 创建副本并前进位置指针
    new_state = parser_state.copy()
    new_state["pos"] = pos + 1
    
    return new_state

# === helper functions ===
# No helper functions needed for this simple utility

# === OOP compatibility layer ===
# Not required for this utility function
