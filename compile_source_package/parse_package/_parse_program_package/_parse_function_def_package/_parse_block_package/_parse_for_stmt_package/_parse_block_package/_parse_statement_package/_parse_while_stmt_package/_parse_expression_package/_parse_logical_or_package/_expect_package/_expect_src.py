# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._current_token_package._current_token_src import _current_token

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
def _expect(parser_state: ParserState, token_type: str) -> Token:
    """期望并消耗指定类型的 token。
    
    如果当前 token 类型匹配，消耗它并返回；否则抛出 SyntaxError。
    """
    current = _current_token(parser_state)
    
    if current["type"] == token_type:
        parser_state["pos"] += 1
        return current
    else:
        raise SyntaxError(
            f"Expected token type '{token_type}', got '{current['type']}' "
            f"at line {current['line']}, column {current['column']} "
            f"in file '{parser_state.get('filename', '<unknown>')}'"
        )

# === helper functions ===

# === OOP compatibility layer ===
