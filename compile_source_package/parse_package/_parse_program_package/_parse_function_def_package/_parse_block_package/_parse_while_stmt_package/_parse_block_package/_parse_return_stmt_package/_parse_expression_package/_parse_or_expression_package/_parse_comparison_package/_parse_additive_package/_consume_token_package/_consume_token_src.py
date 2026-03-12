# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple token consumption logic

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
def _consume_token(parser_state: ParserState) -> ParserState:
    """
    消费当前 token（前进位置）。
    
    从 parser_state 中获取 tokens 列表和 pos 位置，如果 pos < len(tokens)，
    创建新的 parser_state 副本并将 pos 加 1；如果已在末尾则保持原位置不变。
    不修改原字典，返回新字典。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # Check if there are more tokens to consume
    if pos < len(tokens):
        # Create a new copy with pos incremented
        new_state = dict(parser_state)
        new_state["pos"] = pos + 1
        return new_state
    else:
        # Already at end, return copy with unchanged pos
        return dict(parser_state)

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a helper function, not a framework entry point
