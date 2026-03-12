# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_block_package._parse_block_src import _parse_block

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
def _parse_for_stmt(parser_state: ParserState) -> AST:
    """
    Parse for statement.
    
    Grammar:
    for_stmt := FOR LPAREN LET IDENTIFIER EQUALS expression RPAREN block
    block := COLON statement* SEMICOLON
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. Consume FOR keyword
    if pos >= len(tokens) or tokens[pos]["type"] != "FOR":
        raise SyntaxError(f"Expected FOR keyword at line {tokens[pos]['line'] if pos < len(tokens) else 'EOF'}")
    for_token = tokens[pos]
    pos += 1
    
    # 2. Consume LPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "LPAREN":
        raise SyntaxError(f"Expected '(' at line {tokens[pos]['line'] if pos < len(tokens) else 'EOF'}")
    pos += 1
    
    # 3. Consume LET keyword
    if pos >= len(tokens) or tokens[pos]["type"] != "LET":
        raise SyntaxError(f"Expected LET keyword at line {tokens[pos]['line'] if pos < len(tokens) else 'EOF'}")
    pos += 1
    
    # 4. Consume iteration variable identifier
    if pos >= len(tokens) or tokens[pos]["type"] != "IDENTIFIER":
        raise SyntaxError(f"Expected iteration variable at line {tokens[pos]['line'] if pos < len(tokens) else 'EOF'}")
    iter_var_token = tokens[pos]
    pos += 1
    
    # 5. Consume EQUALS
    if pos >= len(tokens) or tokens[pos]["type"] != "EQUALS":
        raise SyntaxError(f"Expected '=' at line {tokens[pos]['line'] if pos < len(tokens) else 'EOF'}")
    pos += 1
    
    # 6. Parse iterable expression
    parser_state["pos"] = pos
    iterable_ast = _parse_expression(parser_state)
    pos = parser_state["pos"]
    
    # 7. Consume RPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "RPAREN":
        raise SyntaxError(f"Expected ')' at line {tokens[pos]['line'] if pos < len(tokens) else 'EOF'}")
    pos += 1
    
    # 8. Consume COLON (block start marker)
    if pos >= len(tokens) or tokens[pos]["type"] != "COLON":
        raise SyntaxError(f"Expected ':' at line {tokens[pos]['line'] if pos < len(tokens) else 'EOF'}")
    pos += 1
    
    # 9. Parse statement block
    parser_state["pos"] = pos
    block_ast = _parse_block(parser_state)
    pos = parser_state["pos"]
    
    # 10. Build FOR AST node
    for_ast = {
        "type": "FOR",
        "line": for_token["line"],
        "column": for_token["column"],
        "children": [
            {
                "type": "ITER_VAR",
                "value": iter_var_token["value"],
                "line": iter_var_token["line"],
                "column": iter_var_token["column"]
            },
            iterable_ast,
            block_ast
        ]
    }
    
    parser_state["pos"] = pos
    return for_ast

# === helper functions ===
# None - all logic is in main function, sub-functions are delegated

# === OOP compatibility layer ===
# Not needed - this is a parser helper function, not a framework entry point
