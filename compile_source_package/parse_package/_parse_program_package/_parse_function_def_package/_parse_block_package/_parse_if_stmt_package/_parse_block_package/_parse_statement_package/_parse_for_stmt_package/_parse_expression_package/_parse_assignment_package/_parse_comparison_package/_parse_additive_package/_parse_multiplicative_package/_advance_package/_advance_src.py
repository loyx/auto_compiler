# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions required for this simple helper

# === ADT defines ===
ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _advance(parser_state: ParserState) -> None:
    """
    将 parser_state['pos'] 前进到下一个位置。
    
    行为：
    1. 将 parser_state['pos'] 加 1
    2. 不检查边界（由调用者负责确保不越界）
    
    副作用：修改 parser_state['pos']
    """
    parser_state['pos'] += 1

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this helper function