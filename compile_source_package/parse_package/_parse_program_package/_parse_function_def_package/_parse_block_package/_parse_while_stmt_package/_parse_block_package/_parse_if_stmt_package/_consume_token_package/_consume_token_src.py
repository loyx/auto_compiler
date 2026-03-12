# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this utility function

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
def _consume_token(parser_state: ParserState, token_type: str) -> ParserState:
    """
    消费指定类型的 token。
    
    如果当前 token 类型匹配期望的 token_type，返回更新后的 parser_state（pos+1）。
    如果不匹配或已到达末尾，抛出 SyntaxError。
    
    不修改原始 parser_state，返回更新后的副本。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if position is valid
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input: expected {token_type}")
    
    # Get current token
    current_token = tokens[pos]
    actual_type = current_token["type"]
    
    # Check if token type matches
    if actual_type != token_type:
        line = current_token.get("line", "?")
        column = current_token.get("column", "?")
        raise SyntaxError(
            f"Expected token type {token_type}, got {actual_type} at line {line}:column {column}"
        )
    
    # Return updated parser_state copy with pos incremented
    new_state = parser_state.copy()
    new_state["pos"] = pos + 1
    return new_state

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function