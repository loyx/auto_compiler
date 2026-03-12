from typing import Any, Dict

Token = Dict[str, Any]
ParserState = Dict[str, Any]

def _consume_token(state: ParserState) -> Token:
    """Consume and return current token."""
    pos = state.get("pos", 0)
    tokens = state.get("tokens", [])
    if pos < len(tokens):
        state["pos"] = pos + 1
        return tokens[pos]
    return None
