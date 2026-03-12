# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_dict_literal_package._parse_dict_literal_src import _parse_dict_literal
from ._parse_list_literal_package._parse_list_literal_src import _parse_list_literal
from ._parse_tuple_literal_package._parse_tuple_literal_src import _parse_tuple_literal
from ._parse_atom_package._parse_atom_src import _parse_atom

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
    解析任意表达式。这是表达式解析的入口函数。
    根据第一个 token 的类型分发到不同的解析逻辑。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否越界
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input at {parser_state.get('filename', 'unknown')}")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    # 根据 token 类型分发到不同的解析逻辑
    if token_type == "LEFT_BRACE":
        result = _parse_dict_literal(parser_state)
    elif token_type == "LEFT_BRACKET":
        result = _parse_list_literal(parser_state)
    elif token_type == "LEFT_PAREN":
        result = _parse_tuple_literal(parser_state)
    elif token_type in ("STRING", "NUMBER", "IDENTIFIER", "TRUE", "FALSE", "NONE"):
        result = _parse_atom(parser_state)
    elif token_type in ("PLUS", "MINUS", "STAR", "SLASH", "PERCENT"):
        # 一元运算符表达式
        result = _parse_unary_expression(parser_state)
    elif token_type == "NOT":
        # 逻辑非表达式
        result = _parse_unary_expression(parser_state)
    else:
        raise SyntaxError(
            f"Unexpected token '{token_type}' at line {current_token.get('line', '?')}, "
            f"column {current_token.get('column', '?')}"
        )
    
    return result

# === helper functions ===
def _parse_unary_expression(parser_state: ParserState) -> AST:
    """
    解析一元表达式（如 -x, +x, not x）。
    这是一个简单的 helper，实际逻辑可能委托给更专门的子函数。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    operator_token = tokens[pos]
    
    # 推进到操作符之后
    parser_state["pos"] = pos + 1
    
    # 解析操作数（递归调用 _parse_expression）
    operand = _parse_expression(parser_state)
    
    return {
        "type": "UNARY_OP",
        "operator": operator_token["value"],
        "operand": operand,
        "line": operator_token.get("line"),
        "column": operator_token.get("column")
    }

# === OOP compatibility layer ===
# Not needed for this parser function node
