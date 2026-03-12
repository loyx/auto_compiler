# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Note: Import is done inside the function to avoid circular dependency
# with _parse_expression which also imports this module.

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
def _parse_function_call(parser_state: ParserState, identifier_ast: AST, lparen_token: Token) -> AST:
    """Parse function call arguments after LPAREN and return CALL AST node."""
    # Import inside function to avoid circular dependency
    from ._parse_expression_package._parse_expression_src import _parse_expression
    
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    arguments = []
    
    # Check for empty parameter list (immediate RPAREN)
    if pos < len(tokens) and tokens[pos]["type"] == "RPAREN":
        parser_state["pos"] = pos + 1
        return {
            "type": "CALL",
            "callee": identifier_ast,
            "arguments": arguments,
            "line": lparen_token["line"],
            "column": lparen_token["column"]
        }
    
    # Parse first argument
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input while parsing function arguments")
    
    arg_ast = _parse_expression(parser_state)
    arguments.append(arg_ast)
    
    # Parse remaining arguments (comma-separated)
    while True:
        pos = parser_state["pos"]
        if pos >= len(tokens):
            raise SyntaxError("Unexpected end of input while parsing function arguments")
        
        current_token = tokens[pos]
        
        if current_token["type"] == "COMMA":
            parser_state["pos"] = pos + 1
            arg_ast = _parse_expression(parser_state)
            arguments.append(arg_ast)
        elif current_token["type"] == "RPAREN":
            parser_state["pos"] = pos + 1
            break
        else:
            raise SyntaxError(
                f"Expected ',' or ')' after argument, got '{current_token['value']}' "
                f"at line {current_token['line']}, column {current_token['column']}"
            )
    
    return {
        "type": "CALL",
        "callee": identifier_ast,
        "arguments": arguments,
        "line": lparen_token["line"],
        "column": lparen_token["column"]
    }

# === helper functions ===

# === OOP compatibility layer ===
