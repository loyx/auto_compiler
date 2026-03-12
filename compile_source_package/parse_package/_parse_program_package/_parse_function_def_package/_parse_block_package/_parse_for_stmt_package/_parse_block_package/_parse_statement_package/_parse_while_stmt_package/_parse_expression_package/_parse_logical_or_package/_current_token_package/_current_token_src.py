# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed

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
def _current_token(parser_state: ParserState) -> Token:
    """获取当前位置的 token。
    
    如果 pos 在 tokens 范围内，返回 tokens[pos]。
    如果超出范围，返回 EOF token。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos < len(tokens):
        return tokens[pos]
    else:
        return {
            "type": "EOF",
            "value": "",
            "line": 0,
            "column": 0
        }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
