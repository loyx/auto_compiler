# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_expression_package._parse_multiplicative_expression_src import _parse_multiplicative_expression

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
def _parse_additive_expression(parser_state: ParserState) -> AST:
    """
    解析加法表达式（支持 + 和 - 运算符）。
    原地修改 parser_state['pos'] 到表达式结束位置。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 解析左操作数
    left = _parse_multiplicative_expression(parser_state)
    
    # 循环处理 + 和 - 运算符
    while parser_state["pos"] < len(tokens):
        token = tokens[parser_state["pos"]]
        
        if token["type"] != "OPERATOR" or token["value"] not in ("+", "-"):
            break
        
        # 记录运算符
        op_token = token
        parser_state["pos"] += 1
        
        # 解析右操作数
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(
                f"Expected operand after '{op_token['value']}' at "
                f"line {op_token['line']}, column {op_token['column']}"
            )
        
        right = _parse_multiplicative_expression(parser_state)
        
        # 构建 BINARY_OP 节点
        left = {
            "type": "BINARY_OP",
            "value": op_token["value"],
            "children": [left, right],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function