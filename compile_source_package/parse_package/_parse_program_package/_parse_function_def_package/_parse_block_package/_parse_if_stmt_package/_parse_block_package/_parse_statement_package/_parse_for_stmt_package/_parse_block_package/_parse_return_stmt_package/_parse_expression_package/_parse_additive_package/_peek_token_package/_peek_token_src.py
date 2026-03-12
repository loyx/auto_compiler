from typing import Any, Dict

Token = Dict[str, Any]
ParserState = Dict[str, Any]

def _peek_token(state: ParserState) -> Token:
    """Return current token or None if at end."""
    pos = state.get("pos", 0)
    tokens = state.get("tokens", [])
    if pos < len(tokens):
        return tokens[pos]
    return None
