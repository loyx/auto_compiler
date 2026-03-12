# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub-functions needed for this atomic parser

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,         # Token type: "STRING", "NUMBER", "IDENTIFIER", "TRUE", "FALSE", "NONE"
#   "value": str,        # Raw token value as string
#   "line": int,         # Line number in source
#   "column": int        # Column number in source
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,         # AST node type: "string", "number", "identifier", "boolean", "none"
#   "children": list,    # Child nodes (empty for atoms)
#   "value": Any,        # Parsed value (str, int, float, bool, None)
#   "line": int,         # Source line number
#   "column": int        # Source column number
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,      # List of Token objects
#   "filename": str,     # Source filename
#   "pos": int,          # Current position in tokens list
#   "error": str         # Error message (if any)
# }


# === main function ===
def _parse_atom(parser_state: ParserState) -> AST:
    """
    Parse atomic values (strings, numbers, identifiers, booleans, None).
    
    Args:
        parser_state: ParserState with pos pointing to an atomic token
        
    Returns:
        AST node representing the atomic value
        
    Raises:
        SyntaxError: If token type is unknown or position is out of bounds
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Boundary check
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input at {parser_state.get('filename', '<unknown>')}")
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    token_line = token.get("line", 0)
    token_column = token.get("column", 0)
    
    # Parse based on token type
    if token_type == "STRING":
        # Remove quotes from string value
        parsed_value = token_value[1:-1] if len(token_value) >= 2 else token_value
        ast_node = _create_atom_node("string", parsed_value, token_line, token_column)
    elif token_type == "NUMBER":
        # Distinguish int vs float based on decimal point
        parsed_value = _parse_number_value(token_value)
        ast_node = _create_atom_node("number", parsed_value, token_line, token_column)
    elif token_type == "IDENTIFIER":
        # Keep identifier name as-is
        ast_node = _create_atom_node("identifier", token_value, token_line, token_column)
    elif token_type == "TRUE":
        ast_node = _create_atom_node("boolean", True, token_line, token_column)
    elif token_type == "FALSE":
        ast_node = _create_atom_node("boolean", False, token_line, token_column)
    elif token_type == "NONE":
        ast_node = _create_atom_node("none", None, token_line, token_column)
    else:
        raise SyntaxError(
            f"Unexpected token type '{token_type}' at line {token_line}, "
            f"column {token_column} in {parser_state.get('filename', '<unknown>')}"
        )
    
    # Advance position
    parser_state["pos"] = pos + 1
    
    return ast_node


# === helper functions ===
def _create_atom_node(node_type: str, value: Any, line: int, column: int) -> AST:
    """
    Create an atomic AST node with consistent structure.
    
    Args:
        node_type: AST node type string
        value: Parsed value
        line: Source line number
        column: Source column number
        
    Returns:
        AST node dictionary
    """
    return {
        "type": node_type,
        "children": [],
        "value": value,
        "line": line,
        "column": column
    }


def _parse_number_value(token_value: str) -> Any:
    """
    Parse a number token value into int or float.
    
    Args:
        token_value: Raw number string from token
        
    Returns:
        int if no decimal point, float otherwise
    """
    if "." in token_value or "e" in token_value.lower():
        return float(token_value)
    else:
        return int(token_value)


# === OOP compatibility layer ===
# Not needed: this is a helper parser function, not a framework entry point
