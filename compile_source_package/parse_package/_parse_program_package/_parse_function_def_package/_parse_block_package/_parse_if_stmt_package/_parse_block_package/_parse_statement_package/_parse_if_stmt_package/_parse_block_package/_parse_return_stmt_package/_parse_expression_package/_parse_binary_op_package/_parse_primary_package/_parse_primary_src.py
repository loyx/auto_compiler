# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_primary(parser_state: ParserState) -> AST:
    """
    Parse primary expression (literals, identifiers, parenthesized expressions, unary operators).
    Input: parser_state with pos pointing to the token to parse.
    Output: AST node or None if cannot parse.
    Side effect: modifies parser_state["pos"] to end of expression.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos >= len(tokens):
        return None
    
    token = tokens[pos]
    token_type = token["type"]
    
    # Handle literals: NUMBER, STRING, TRUE, FALSE, NULL
    if token_type in ("NUMBER", "STRING", "TRUE", "FALSE", "NULL"):
        parser_state["pos"] = pos + 1
        return {
            "type": token_type,
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    # Handle identifier
    if token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {
            "type": "IDENTIFIER",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    # Handle parenthesized expression: LPAREN ... RPAREN
    if token_type == "LPAREN":
        parser_state["pos"] = pos + 1  # Skip LPAREN
        expr = _parse_binary_op(parser_state)
        
        if expr is None:
            raise SyntaxError(f"{filename}:{token['line']}:{token['column']}: Expected expression after '('")
        
        # Check for closing parenthesis
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens) or tokens[new_pos]["type"] != "RPAREN":
            raise SyntaxError(f"{filename}:{token['line']}:{token['column']}: Expected closing parenthesis")
        
        parser_state["pos"] = new_pos + 1  # Skip RPAREN
        return expr
    
    # Handle unary minus: MINUS <expression>
    if token_type == "MINUS":
        parser_state["pos"] = pos + 1  # Skip MINUS
        operand = _parse_binary_op(parser_state)
        
        if operand is None:
            raise SyntaxError(f"{filename}:{token['line']}:{token['column']}: Expected expression after unary minus")
        
        return {
            "type": "UNARY_OP",
            "operator": "MINUS",
            "operand": operand,
            "line": token["line"],
            "column": token["column"]
        }
    
    # Cannot parse this token as primary expression
    return None

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
