# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_or_expr_package._parse_or_expr_src import _parse_or_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }


# === main function ===
def _parse_primary(parser_state: ParserState) -> AST:
    """Parse primary expression (literals, identifiers, parentheses)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    line = token["line"]
    column = token["column"]
    
    if token_type == "NUMBER":
        # Parse number literal (int or float)
        parser_state["pos"] = pos + 1
        if "." in token_value:
            value = float(token_value)
        else:
            value = int(token_value)
        return {
            "type": "LITERAL",
            "children": [],
            "value": value,
            "line": line,
            "column": column
        }
    
    elif token_type == "STRING":
        # Parse string literal (remove quotes)
        parser_state["pos"] = pos + 1
        # Remove surrounding quotes (either ' or ")
        if (token_value.startswith('"') and token_value.endswith('"')) or \
           (token_value.startswith("'") and token_value.endswith("'")):
            value = token_value[1:-1]
        else:
            value = token_value
        return {
            "type": "LITERAL",
            "children": [],
            "value": value,
            "line": line,
            "column": column
        }
    
    elif token_type == "BOOL":
        # Parse boolean literal
        parser_state["pos"] = pos + 1
        value = token_value.lower() == "true"
        return {
            "type": "LITERAL",
            "children": [],
            "value": value,
            "line": line,
            "column": column
        }
    
    elif token_type == "NONE":
        # Parse none literal
        parser_state["pos"] = pos + 1
        return {
            "type": "LITERAL",
            "children": [],
            "value": None,
            "line": line,
            "column": column
        }
    
    elif token_type == "IDENTIFIER":
        # Parse identifier reference
        parser_state["pos"] = pos + 1
        return {
            "type": "IDENTIFIER",
            "children": [],
            "value": token_value,
            "line": line,
            "column": column
        }
    
    elif token_type == "LPAREN":
        # Parse parenthesized expression
        parser_state["pos"] = pos + 1  # consume "("
        expr_node = _parse_or_expr(parser_state)
        
        # Check for closing parenthesis
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens) or tokens[new_pos]["type"] != "RPAREN":
            raise SyntaxError(f"Expected ')' at line {line}")
        
        parser_state["pos"] = new_pos + 1  # consume ")"
        return expr_node
    
    else:
        # Not a valid expression start token
        raise SyntaxError(f"Expected expression at line {line}")


# === helper functions ===
# No helper functions needed for this implementation


# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
