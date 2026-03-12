# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_package._parse_unary_src import _parse_unary
from ._parse_binary_op_package._parse_binary_op_src import _parse_binary_op

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

# Expression-ending tokens
EXPR_END_TOKENS = {"SEMICOLON", "RPAREN", "COMMA", "RBRACE", "RBRACKET", "NEWLINE", "EOF"}

# === main function ===
def _parse_expression(parser_state: dict) -> dict:
    """Parse expression until expression-ending token.
    
    Args:
        parser_state: Parser state with pos at expression start token.
        
    Returns:
        Expression AST node.
        
    Side effects:
        Updates parser_state['pos'] to point after the expression.
        
    Raises:
        SyntaxError: On invalid token or syntax error.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # Check for empty expression (should be handled by caller, but guard here)
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input")
    
    token = tokens[pos]
    if token["type"] in EXPR_END_TOKENS:
        raise SyntaxError(f"{filename}:{token['line']}:{token['column']}: Unexpected token '{token['value']}'")
    
    # Parse expression starting with unary (which calls _parse_primary internally)
    expr = _parse_unary(parser_state)
    
    # Continue with binary operations using precedence climbing
    expr = _parse_binary_op(parser_state, 0)
    
    return expr

# === helper functions ===
def _is_expression_end(token_type: str) -> bool:
    """Check if token type indicates expression end."""
    return token_type in EXPR_END_TOKENS

# === OOP compatibility layer ===
# No OOP wrapper needed for parser helper function
