# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_package._parse_comparison_src import _parse_comparison

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
def _parse_and_expression(parser_state: ParserState) -> AST:
    """
    解析逻辑与表达式。处理 `&&` 运算符，构建左结合 AST。
    原地修改 parser_state["pos"]。
    """
    tokens = parser_state["tokens"]
    
    # 先解析左操作数
    left = _parse_comparison(parser_state)
    
    # 循环处理 && 运算符
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        # 检查是否为 && 运算符
        if current_token["type"] != "OPERATOR" or current_token["value"] != "&&":
            break
        
        # 记录运算符 token 并前进
        op_token = current_token
        parser_state["pos"] += 1
        
        # 检查是否有右操作数
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(
                f"Expected expression after '&&' at line {op_token['line']}, column {op_token['column']}"
            )
        
        # 解析右操作数
        right = _parse_comparison(parser_state)
        
        # 构建 BINARY_OP 节点（左结合）
        left = {
            "type": "BINARY_OP",
            "value": "&&",
            "line": op_token["line"],
            "column": op_token["column"],
            "children": [left, right]
        }
    
    return left


# === helper functions ===
# No helper functions needed for this simple parsing logic

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function nodes
