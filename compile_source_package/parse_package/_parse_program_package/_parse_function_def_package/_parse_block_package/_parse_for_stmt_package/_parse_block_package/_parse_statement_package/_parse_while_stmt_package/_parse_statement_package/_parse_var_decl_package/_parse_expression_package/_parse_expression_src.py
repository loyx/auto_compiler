# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub-functions for this basic framework implementation

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,        # e.g., "NUMBER", "STRING", "IDENTIFIER", "OPERATOR", "LPAREN", "RPAREN"
#   "value": str,       # token value
#   "line": int,        # line number in source
#   "column": int       # column number in source
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,        # e.g., "BinaryOp", "Literal", "Identifier"
#   "children": list,   # child AST nodes
#   "value": Any,       # node value (for literals/identifiers)
#   "line": int,        # line number
#   "column": int,      # column number
#   "operator": str     # operator for BinaryOp nodes
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,     # List[Token]
#   "pos": int,         # current position in token list
#   "filename": str,    # source filename
#   "error": str        # error message (if any)
# }

# === main function ===
def _parse_expression(parser_state: ParserState) -> AST:
    """
    Parse expression from current position in parser_state.
    Consumes all expression tokens and returns AST node.
    Updates parser_state["pos"] to position after expression.
    Raises SyntaxError on invalid expression syntax.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of expression")
    
    # Parse left side of expression
    left_node = _parse_primary(parser_state)
    
    # Parse binary operators (left-associative)
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        if current_token["type"] != "OPERATOR":
            break
        
        operator = current_token["value"]
        if operator not in ["+", "-", "*", "/"]:
            break
        
        # Consume operator
        parser_state["pos"] += 1
        
        # Parse right side
        right_node = _parse_primary(parser_state)
        
        # Create binary operation node
        left_node = {
            "type": "BinaryOp",
            "operator": operator,
            "children": [left_node, right_node],
            "line": current_token["line"],
            "column": current_token["column"]
        }
    
    return left_node

# === helper functions ===
def _parse_primary(parser_state: ParserState) -> AST:
    """
    Parse primary expression: literal, identifier, or parenthesized expression.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of expression")
    
    token = tokens[pos]
    
    # Handle parenthesized expression
    if token["type"] == "LPAREN":
        parser_state["pos"] += 1  # consume '('
        expr_node = _parse_expression(parser_state)
        
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(f"{filename}:{token['line']}:{token['column']}: Unclosed parenthesis")
        
        closing = tokens[parser_state["pos"]]
        if closing["type"] != "RPAREN":
            raise SyntaxError(f"{filename}:{closing['line']}:{closing['column']}: Expected ')', got '{closing['value']}'")
        
        parser_state["pos"] += 1  # consume ')'
        return expr_node
    
    # Handle literals (numbers, strings)
    if token["type"] in ["NUMBER", "STRING"]:
        parser_state["pos"] += 1
        return {
            "type": "Literal",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    # Handle identifiers
    if token["type"] == "IDENTIFIER":
        parser_state["pos"] += 1
        return {
            "type": "Identifier",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    # Unknown token type for primary expression
    raise SyntaxError(f"{filename}:{token['line']}:{token['column']}: Unexpected token '{token['value']}' in expression")

# === OOP compatibility layer ===
# Not required for this parser function node
