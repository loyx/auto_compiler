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
def _parse_if_stmt(parser_state: ParserState) -> AST:
    """Parse an if-elif-else statement and return an IF_STMT AST node."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]

    # Get IF token position
    if_token = tokens[pos]
    line = if_token["line"]
    column = if_token["column"]

    # 1. Consume IF token
    parser_state["pos"] += 1

    # 2. Parse condition expression
    condition_ast = _parse_expression(parser_state)

    # 3. Expect COLON after condition
    pos = parser_state["pos"]
    if pos >= len(tokens) or tokens[pos]["type"] != "COLON":
        raise SyntaxError(f"Expected COLON after if condition at line {line}, column {column}")
    parser_state["pos"] += 1

    # 4. Parse if block
    if_block = _parse_block(parser_state)

    # Build children list
    children = [condition_ast, if_block]

    # 5. Handle optional ELIF branches
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        if current_token["type"] == "ELIF":
            elif_line = current_token["line"]
            elif_column = current_token["column"]
            parser_state["pos"] += 1

            # Parse elif condition
            elif_condition = _parse_expression(parser_state)

            # Expect COLON
            pos = parser_state["pos"]
            if pos >= len(tokens) or tokens[pos]["type"] != "COLON":
                raise SyntaxError(
                    f"Expected COLON after elif condition at line {elif_line}, column {elif_column}"
                )
            parser_state["pos"] += 1

            # Parse elif block
            elif_block = _parse_block(parser_state)

            # Add ELIF_BRANCH node
            elif_branch: AST = {
                "type": "ELIF_BRANCH",
                "line": elif_line,
                "column": elif_column,
                "children": [elif_condition, elif_block]
            }
            children.append(elif_branch)
        else:
            break

    # 6. Handle optional ELSE branch
    if parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        if current_token["type"] == "ELSE":
            else_line = current_token["line"]
            else_column = current_token["column"]
            parser_state["pos"] += 1

            # Expect COLON
            pos = parser_state["pos"]
            if pos >= len(tokens) or tokens[pos]["type"] != "COLON":
                raise SyntaxError(
                    f"Expected COLON after else at line {else_line}, column {else_column}"
                )
            parser_state["pos"] += 1

            # Parse else block
            else_block = _parse_block(parser_state)

            # Add ELSE_BRANCH node
            else_branch: AST = {
                "type": "ELSE_BRANCH",
                "line": else_line,
                "column": else_column,
                "children": [else_block]
            }
            children.append(else_branch)

    # Build and return IF_STMT AST node
    result: AST = {
        "type": "IF_STMT",
        "line": line,
        "column": column,
        "children": children
    }
    return result


# === helper functions ===


# === OOP compatibility layer ===
