# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_factor_package._parse_factor_src import _parse_factor

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
#   "column": int,
#   "operator": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST
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
def _parse_term(parser_state: ParserState) -> AST:
    """Parse additive (+, -) expressions. Priority: higher than factor, lower than comparison."""
    left = _parse_factor(parser_state)
    
    while _is_at_token(parser_state) and _current_token_value(parser_state) in ('+', '-'):
        op_token = _consume_token(parser_state)
        op_value = op_token['value']
        op_line = op_token['line']
        op_column = op_token['column']
        
        right = _parse_factor(parser_state)
        
        left = {
            "type": "BINARY",
            "operator": op_value,
            "left": left,
            "right": right,
            "line": op_line,
            "column": op_column
        }
    
    return left

# === helper functions ===
def _is_at_token(parser_state: ParserState) -> bool:
    """Check if parser position is within token bounds."""
    return parser_state['pos'] < len(parser_state['tokens'])

def _current_token_value(parser_state: ParserState) -> str:
    """Get value of current token without consuming it."""
    if not _is_at_token(parser_state):
        raise SyntaxError(f"Unexpected end of input in {parser_state.get('filename', 'unknown')}")
    return parser_state['tokens'][parser_state['pos']]['value']

def _consume_token(parser_state: ParserState) -> Token:
    """Consume and return current token, advancing position."""
    if not _is_at_token(parser_state):
        raise SyntaxError(f"Unexpected end of input in {parser_state.get('filename', 'unknown')}")
    token = parser_state['tokens'][parser_state['pos']]
    parser_state['pos'] += 1
    return token

# === OOP compatibility layer ===
