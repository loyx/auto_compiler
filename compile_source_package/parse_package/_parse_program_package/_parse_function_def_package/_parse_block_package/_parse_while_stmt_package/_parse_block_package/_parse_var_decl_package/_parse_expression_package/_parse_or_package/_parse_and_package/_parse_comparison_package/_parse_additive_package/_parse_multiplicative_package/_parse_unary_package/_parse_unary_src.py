# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
from ._consume_token_package._consume_token_src import _consume_token

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
def _parse_unary(parser_state: ParserState) -> Tuple[AST, ParserState]:
    """Parse unary expression (prefix +/- operators and atomic expressions)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(
            f"Syntax error at {parser_state['filename']}: unexpected end of input"
        )
    
    current_token = tokens[pos]
    
    if current_token["type"] in ("PLUS", "MINUS"):
        op_token, new_state = _consume_token(parser_state, current_token["type"])
        operand_ast, final_state = _parse_unary(new_state)
        
        return {
            "type": "UNARY_OP",
            "value": op_token["value"],
            "children": [operand_ast],
            "line": op_token["line"],
            "column": op_token["column"]
        }, final_state
    else:
        return _parse_primary(parser_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for parser function nodes