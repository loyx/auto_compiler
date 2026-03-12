# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No child functions needed for this implementation

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
def _parse_expression(parser_state: ParserState) -> AST:
    """
    Parse an expression from the current position in parser_state.
    Supports literals (NUMBER, STRING), identifiers (IDENT),
    binary operations (+, -, *, /), and parenthesized expressions.
    Modifies parser_state['pos'] to consume tokens.
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # Check if we have tokens to parse
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input while parsing expression"
        return {"type": "ERROR", "value": "Unexpected end of input", "line": 0, "column": 0}
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    token_value = current_token.get("value", "")
    token_line = current_token.get("line", 0)
    token_column = current_token.get("column", 0)
    
    # Parse first operand
    first_operand: Optional[AST] = None
    
    if token_type in ("NUMBER", "STRING"):
        # Literal value
        parser_state["pos"] = pos + 1
        first_operand = {
            "type": token_type,
            "value": token_value,
            "line": token_line,
            "column": token_column
        }
    elif token_type == "IDENT":
        # Identifier
        parser_state["pos"] = pos + 1
        first_operand = {
            "type": "IDENTIFIER",
            "value": token_value,
            "line": token_line,
            "column": token_column
        }
    elif token_type == "LPAREN":
        # Parenthesized expression: consume '(' and parse inner expression
        parser_state["pos"] = pos + 1
        first_operand = _parse_expression(parser_state)
        # Expect closing ')'
        new_pos = parser_state.get("pos", 0)
        if new_pos < len(tokens) and tokens[new_pos].get("type") == "RPAREN":
            parser_state["pos"] = new_pos + 1
        else:
            parser_state["error"] = "Expected closing parenthesis ')'"
            first_operand["type"] = "ERROR"
    else:
        # Unexpected token
        parser_state["error"] = f"Unexpected token '{token_type}' while parsing expression"
        parser_state["pos"] = pos + 1
        return {
            "type": "ERROR",
            "value": f"Unexpected token: {token_type}",
            "line": token_line,
            "column": token_column
        }
    
    # Check for binary operator
    current_pos = parser_state.get("pos", 0)
    if current_pos >= len(tokens):
        return first_operand
    
    next_token = tokens[current_pos]
    next_type = next_token.get("type", "")
    
    binary_operators = {"PLUS": "+", "MINUS": "-", "STAR": "*", "SLASH": "/"}
    
    if next_type in binary_operators:
        # Consume operator
        parser_state["pos"] = current_pos + 1
        operator = binary_operators[next_type]
        op_line = next_token.get("line", token_line)
        op_column = next_token.get("column", token_column)
        
        # Parse right operand
        right_operand = _parse_expression(parser_state)
        
        # Return binary operation AST
        return {
            "type": "BINARY_OP",
            "left": first_operand,
            "operator": operator,
            "right": right_operand,
            "line": token_line,
            "column": token_column
        }
    
    # No binary operator, return first operand
    return first_operand

# === helper functions ===
# No helper functions needed - logic is contained in main function

# === OOP compatibility layer ===
# Not needed - this is a parser helper function, not a framework entry point
