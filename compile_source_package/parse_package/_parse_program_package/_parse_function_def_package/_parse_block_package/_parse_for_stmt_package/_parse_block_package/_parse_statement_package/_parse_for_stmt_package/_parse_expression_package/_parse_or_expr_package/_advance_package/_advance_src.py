# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed

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
def _advance(parser_state: ParserState) -> Token:
    """
    Advance to next token and return the current token.
    
    Side effect: Mutates parser_state["pos"] += 1 in place.
    No error handling for out-of-range positions.
    """
    current_token = parser_state["tokens"][parser_state["pos"]]
    parser_state["pos"] += 1
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function