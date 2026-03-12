# === std / third-party imports ===
from typing import Any, Dict

# === ADT defines ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]

# === main function ===
def _parse_multiplicative(state: ParserState) -> AST:
    """Stub implementation for _parse_multiplicative."""
    return {"type": "STUB", "value": "multiplicative", "line": 0, "column": 0}
