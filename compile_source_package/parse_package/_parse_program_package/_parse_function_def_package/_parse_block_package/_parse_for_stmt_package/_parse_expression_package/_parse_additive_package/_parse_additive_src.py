# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_package._parse_multiplicative_src import _parse_multiplicative
from ._is_additive_operator_package._is_additive_operator_src import _is_additive_operator
from ._consume_token_package._consume_token_src import _consume_token
from ._build_binary_op_package._build_binary_op_src import _build_binary_op


# Mock implementations for testing
def _mock_parse_multiplicative(parser_state: dict) -> dict:
    """Mock implementation for testing."""
    return {"type": "MOCK_NUMBER", "value": 0}

def _mock_is_additive_operator(parser_state: dict) -> bool:
    """Mock implementation for testing."""
    return False

def _mock_consume_token(parser_state: dict) -> dict:
    """Mock implementation for testing."""
    return {"type": "PLUS", "value": "+"}

def _mock_build_binary_op(left: dict, right: dict, op_token: dict) -> dict:
    """Mock implementation for testing."""
    return {"type": "BINARY_OP", "value": op_token.get("value")}

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
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
def _parse_additive(parser_state: ParserState) -> AST:
    """Parse additive expression (+, -)."""
    left = _parse_multiplicative(parser_state)
    
    while _is_additive_operator(parser_state):
        op_token = _consume_token(parser_state)
        right = _parse_multiplicative(parser_state)
        left = _build_binary_op(left, right, op_token)
    
    return left

# === helper functions ===
# No helper functions - all logic delegated to child functions

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
