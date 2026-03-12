# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_array_literal_package._parse_array_literal_src import _parse_array_literal
from ._parse_dict_literal_package._parse_dict_literal_src import _parse_dict_literal
from ._parse_number_value_package._parse_number_value_src import _parse_number_value
from ._parse_string_value_package._parse_string_value_src import _parse_string_value
from ._parse_grouping_expr_package._parse_grouping_expr_src import _parse_grouping_expr

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
def _parse_primary_expr(parser_state: ParserState) -> AST:
    """解析主表达式（primary expressions），如标识符、字面量、括号表达式等。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]

    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")

    token = tokens[pos]
    token_type = token["type"]

    if token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {
            "type": "IDENTIFIER",
            "children": [],
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }

    elif token_type == "NUMBER":
        parser_state["pos"] += 1
        value = _parse_number_value(token["value"])
        return {
            "type": "NUMBER_LITERAL",
            "children": [],
            "value": value,
            "line": token["line"],
            "column": token["column"]
        }

    elif token_type == "STRING":
        parser_state["pos"] += 1
        value = _parse_string_value(token["value"])
        return {
            "type": "STRING_LITERAL",
            "children": [],
            "value": value,
            "line": token["line"],
            "column": token["column"]
        }

    elif token_type == "BOOLEAN":
        parser_state["pos"] += 1
        value = token["value"].lower() == "true"
        return {
            "type": "BOOLEAN_LITERAL",
            "children": [],
            "value": value,
            "line": token["line"],
            "column": token["column"]
        }

    elif token_type == "NULL":
        parser_state["pos"] += 1
        return {
            "type": "NULL_LITERAL",
            "children": [],
            "value": None,
            "line": token["line"],
            "column": token["column"]
        }

    elif token_type == "LEFT_PAREN":
        return _parse_grouping_expr(parser_state, token)

    elif token_type == "LEFT_BRACKET":
        return _parse_array_literal(parser_state)

    elif token_type == "LEFT_BRACE":
        return _parse_dict_literal(parser_state)

    else:
        raise SyntaxError(f"Unexpected token '{token['value']}' at line {token['line']}, column {token['column']}")


# === helper functions ===

# === OOP compatibility layer ===
