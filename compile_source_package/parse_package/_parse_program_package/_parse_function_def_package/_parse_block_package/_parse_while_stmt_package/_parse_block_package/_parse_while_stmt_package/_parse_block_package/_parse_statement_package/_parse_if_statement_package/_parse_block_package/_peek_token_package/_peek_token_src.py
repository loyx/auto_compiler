# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# 此函数不调用子函数

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
#   "error": str | None
# }

# === main function ===
def _peek_token(parser_state: ParserState) -> Token | None:
    """
    查看当前 token 但不修改 parser_state 状态。
    
    行为：
    1. 如果 parser_state["pos"] >= len(parser_state["tokens"])，返回 None（表示 EOF）
    2. 否则返回 parser_state["tokens"][parser_state["pos"]]
    
    注意：
    - 不修改 parser_state["pos"]
    - 不抛出异常
    - 返回 Token dict 或 None
    """
    # 获取 tokens 列表和当前位置
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 检查是否超出 tokens 范围
    if pos >= len(tokens):
        return None
    
    # 返回当前 token
    return tokens[pos]

# === helper functions ===
# 此函数无需 helper 函数

# === OOP compatibility layer ===
# 此函数为纯函数，无需 OOP wrapper