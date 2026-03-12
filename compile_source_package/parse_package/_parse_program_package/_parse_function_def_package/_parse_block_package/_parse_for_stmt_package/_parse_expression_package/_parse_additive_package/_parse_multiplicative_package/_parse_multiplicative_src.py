# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Note: Use late binding to avoid circular import with _parse_unary
_parse_unary = None

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
def _parse_multiplicative(parser_state: ParserState) -> AST:
    """Parse multiplicative expressions (*, /)."""
    left = _parse_unary(parser_state)
    
    while parser_state['pos'] < len(parser_state['tokens']):
        token = parser_state['tokens'][parser_state['pos']]
        if token['type'] not in ('STAR', 'SLASH'):
            break
        
        op = token['value']
        parser_state['pos'] += 1
        right = _parse_unary(parser_state)
        
        left = {
            'type': 'BINARY_OP',
            'value': op,
            'children': [left, right],
            'line': left.get('line', token['line']),
            'column': left.get('column', token['column'])
        }
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function nodes
