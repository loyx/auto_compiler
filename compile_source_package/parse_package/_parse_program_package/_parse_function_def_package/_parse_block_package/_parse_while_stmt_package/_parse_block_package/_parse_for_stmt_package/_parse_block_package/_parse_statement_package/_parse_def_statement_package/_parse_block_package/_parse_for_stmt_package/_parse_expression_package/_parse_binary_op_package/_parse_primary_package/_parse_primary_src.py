# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_literal_value_package._parse_literal_value_src import _parse_literal_value

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
def _parse_primary(parser_state: ParserState) -> AST:
    """
    解析初级表达式（字面量、标识符、括号表达式等）。
    副作用：更新 parser_state['pos'] 消费已解析的 token。
    异常：若解析失败抛出 SyntaxError。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input at {parser_state.get('filename', 'unknown')}")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    token_value = current_token["value"]
    token_line = current_token.get("line", 0)
    token_column = current_token.get("column", 0)
    
    # 处理字面量
    if token_type in ("NUMBER", "STRING", "TRUE", "FALSE", "NULL"):
        parser_state["pos"] = pos + 1
        return {
            "type": "Literal",
            "value": _parse_literal_value(token_type, token_value),
            "line": token_line,
            "column": token_column
        }
    
    # 处理标识符
    elif token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {
            "type": "Identifier",
            "value": token_value,
            "line": token_line,
            "column": token_column
        }
    
    # 处理括号表达式
    elif token_type == "LPAREN":
        parser_state["pos"] = pos + 1
        from ._parse_binary_op_package._parse_binary_op_src import _parse_binary_op
        expr = _parse_binary_op(parser_state)
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens) or tokens[new_pos]["type"] != "RPAREN":
            raise SyntaxError(f"Expected ')' at {parser_state.get('filename', 'unknown')}:{token_line}:{token_column}")
        parser_state["pos"] = new_pos + 1
        return {
            "type": "ParenthesizedExpression",
            "children": [expr],
            "line": token_line,
            "column": token_column
        }
    
    # 处理一元运算
    elif token_type in ("MINUS", "BANG"):
        parser_state["pos"] = pos + 1
        operand = _parse_primary(parser_state)
        operator = "-" if token_type == "MINUS" else "!"
        return {
            "type": "UnaryExpression",
            "value": operator,
            "children": [operand],
            "line": token_line,
            "column": token_column
        }
    
    else:
        raise SyntaxError(
            f"Unexpected token '{token_value}' ({token_type}) at "
            f"{parser_state.get('filename', 'unknown')}:{token_line}:{token_column}"
        )

# === helper functions ===
# No helper functions (delegated to sub-function)

# === OOP compatibility layer ===
# Not needed for this parser function
