# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._check_package._check_src import _check
from ._match_package._match_src import _match
from ._previous_package._previous_src import _previous
from ._parse_or_package._parse_or_src import _parse_or

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token type (uppercase string)
#   "value": str,            # token value
#   "line": int,             # line number
#   "column": int            # column number
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # node type (BINARY_OP, UNARY_OP, ASSIGNMENT, etc.)
#   "children": list,        # child nodes (for GROUPING)
#   "value": Any,            # node value (for literals, identifiers)
#   "op": str,               # operator (for BINARY_OP, UNARY_OP)
#   "left": AST,             # left operand (for BINARY_OP)
#   "right": AST,            # right operand (for BINARY_OP)
#   "operand": AST,          # operand (for UNARY_OP)
#   "name": str,             # variable name (for ASSIGNMENT)
#   "line": int,             # line number
#   "column": int            # column number
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # list of Token
#   "pos": int,              # current position
#   "filename": str,         # source filename
#   "error": str             # error message (optional)
# }

# === main function ===
def _parse_assignment(parser_state: ParserState) -> AST:
    """
    Parse assignment expression (lowest precedence level).
    Assignment has right-to-left associativity.
    
    Input: parser_state with parser_state['pos'] pointing to expression start.
    Output: AST node for assignment or delegated expression.
    Updates parser_state['pos'] past the parsed expression.
    """
    # Check for identifier followed by EQUAL (assignment pattern)
    if _check(parser_state, "IDENTIFIER"):
        # Look ahead to check for EQUAL without consuming
        current_pos = parser_state["pos"]
        # Skip the identifier token
        parser_state["pos"] = current_pos + 1
        
        # Check if next token is EQUAL
        if _check(parser_state, "EQUAL"):
            # This is an assignment, consume the identifier
            parser_state["pos"] = current_pos
            identifier_token = _previous(parser_state) if current_pos > 0 else None
            
            # Actually consume the identifier properly
            if current_pos < len(parser_state["tokens"]):
                identifier_token = parser_state["tokens"][current_pos]
                parser_state["pos"] = current_pos + 1
            
            # Consume the EQUAL token
            _match(parser_state, "EQUAL")
            
            # Parse the right-hand side expression (recursive for right-to-left)
            value_ast = _parse_assignment(parser_state)
            
            # Check for parsing errors
            if parser_state.get("error"):
                return _error_node(parser_state, "Invalid assignment value")
            
            # Build assignment AST node
            return {
                "type": "ASSIGNMENT",
                "name": identifier_token["value"],
                "value": value_ast,
                "line": identifier_token["line"],
                "column": identifier_token["column"]
            }
        else:
            # Not an assignment, restore position and fall through
            parser_state["pos"] = current_pos
    
    # Not an assignment, delegate to next precedence level
    return _parse_or(parser_state)

# === helper functions ===
def _error_node(parser_state: ParserState, message: str) -> AST:
    """Create an error AST node and set parser_state error."""
    if not parser_state.get("error"):
        parser_state["error"] = message
    return {
        "type": "ERROR",
        "value": message,
        "line": 0,
        "column": 0
    }

# === OOP compatibility layer ===
# Not required for parser helper function
