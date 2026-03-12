# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._get_current_token_package._get_current_token_src import _get_current_token

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _consume_token(parser_state: ParserState) -> Token:
    """消费当前 token 并前进 pos。"""
    token = _get_current_token(parser_state)
    parser_state["pos"] += 1
    return token

# === helper functions ===

# === OOP compatibility layer ===
