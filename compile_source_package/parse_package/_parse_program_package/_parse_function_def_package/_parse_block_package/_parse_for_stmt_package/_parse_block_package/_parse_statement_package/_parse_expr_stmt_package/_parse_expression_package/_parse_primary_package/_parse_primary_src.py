# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_or_expression_package._parse_or_expression_src import _parse_or_expression
from ._parse_literal_package._parse_literal_src import _parse_literal
from ._parse_identifier_chain_package._parse_identifier_chain_src import _parse_identifier_chain

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
def _parse_primary(parser_state: ParserState) -> AST:
    """Parse primary expression: literals, identifiers, function calls, member access, indexing, grouping."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input at line {parser_state.get('_last_line', 0)}, column {parser_state.get('_last_col', 0)}")
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    line = token["line"]
    column = token["column"]
    
    # 1. Parenthesized expression (grouping)
    if token_value == "(":
        parser_state["pos"] = pos + 1
        inner_expr = _parse_or_expression(parser_state)
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens) or tokens[new_pos]["value"] != ")":
            raise SyntaxError(f"Unexpected end of input, expected ')' at line {line}, column {column}")
        parser_state["pos"] = new_pos + 1
        return inner_expr
    
    # 2. Literals
    if token_type in ("NUMBER", "STRING", "BOOL", "NULL"):
        return _parse_literal(token, parser_state)
    
    # 3. Identifier / variable / function call / member access / indexing
    if token_type == "IDENT":
        return _parse_identifier_chain(token, parser_state)
    
    # 4. Error
    raise SyntaxError(f"Unexpected token '{token_value}' at line {line}, column {column}")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
