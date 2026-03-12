# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression

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
#   "name": str,
#   "callee": AST,
#   "arguments": list,
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
def _parse_function_call(parser_state: ParserState, func_name: str) -> AST:
    """Parse function call expression: LPAREN arguments RPAREN."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Verify and consume LPAREN
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected '('")
    if tokens[pos]["type"] != "LPAREN":
        raise SyntaxError(f"Expected '(', got {tokens[pos]['type']}")
    lparen_token = tokens[pos]
    parser_state["pos"] = pos + 1
    pos = parser_state["pos"]
    
    # Parse arguments
    arguments = []
    if pos < len(tokens) and tokens[pos]["type"] == "RPAREN":
        # Empty argument list
        parser_state["pos"] = pos + 1
    else:
        # Parse first argument
        arguments.append(_parse_expression(parser_state))
        pos = parser_state["pos"]
        
        # Parse remaining arguments (comma-separated)
        while pos < len(tokens) and tokens[pos]["type"] == "COMMA":
            parser_state["pos"] = pos + 1
            pos = parser_state["pos"]
            if pos >= len(tokens):
                raise SyntaxError("Unexpected end of input in argument list")
            arguments.append(_parse_expression(parser_state))
            pos = parser_state["pos"]
        
        # Consume RPAREN
        if pos >= len(tokens):
            raise SyntaxError("Unexpected end of input, expected ')'")
        if tokens[pos]["type"] != "RPAREN":
            raise SyntaxError(f"Expected ')', got {tokens[pos]['type']}")
        parser_state["pos"] = pos + 1
    
    # Build FUNCTION_CALL AST node
    callee_ast = {
        "type": "IDENTIFIER",
        "name": func_name,
        "line": lparen_token["line"],
        "column": lparen_token["column"]
    }
    
    return {
        "type": "FUNCTION_CALL",
        "callee": callee_ast,
        "arguments": arguments,
        "line": lparen_token["line"],
        "column": lparen_token["column"]
    }

# === helper functions ===
# No helper functions needed; logic is delegated to _parse_expression

# === OOP compatibility layer ===
# Not needed for parser function node
