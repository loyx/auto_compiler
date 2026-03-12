# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expression_package._parse_primary_expression_src import _parse_primary_expression

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
def _parse_multiplicative_expression(parser_state: dict) -> dict:
    """
    解析乘法表达式（支持 * 和 / 运算符）。
    输入 parser_state，输出 AST 节点。
    原地修改 parser_state['pos'] 到表达式结束位置。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 解析左操作数
    left_ast = _parse_primary_expression(parser_state)
    
    # 循环处理 * 和 / 运算符
    while parser_state["pos"] < len(tokens):
        token = tokens[parser_state["pos"]]
        
        if token["type"] not in ("MUL", "DIV"):
            break
        
        op_token = token
        op_pos = parser_state["pos"]
        parser_state["pos"] += 1
        
        # 检查是否有右操作数
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(
                f"Expected operand after '{op_token['value']}' "
                f"at {op_token['line']}:{op_token['column']}"
            )
        
        # 解析右操作数
        right_ast = _parse_primary_expression(parser_state)
        
        # 构建 BINARY_OP 节点
        left_ast = {
            "type": "BINARY_OP",
            "operator": op_token["value"],
            "children": [left_ast, right_ast],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node