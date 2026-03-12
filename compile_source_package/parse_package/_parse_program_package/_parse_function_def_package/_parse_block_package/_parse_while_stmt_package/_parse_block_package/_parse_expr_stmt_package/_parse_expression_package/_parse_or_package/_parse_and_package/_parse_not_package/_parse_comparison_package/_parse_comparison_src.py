# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_package._parse_additive_src import _parse_additive

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
def _parse_comparison(parser_state: ParserState) -> AST:
    """
    解析比较表达式（==, !=, <, >, <=, >=）。
    优先级低于 not 一元运算符，高于逻辑运算符。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 解析左操作数（下一优先级：加减表达式）
    left_ast = _parse_additive(parser_state)
    
    # 检查是否还有 token
    if parser_state["pos"] >= len(tokens):
        return left_ast
    
    # 检查当前 token 是否为比较运算符
    current_token = tokens[parser_state["pos"]]
    compare_ops = {"==", "!=", "<", ">", "<=", ">="}
    
    if current_token.get("type") == "COMPARE_OP" and current_token.get("value") in compare_ops:
        op_token = current_token
        op_value = op_token["value"]
        line = op_token.get("line", 0)
        column = op_token.get("column", 0)
        
        # 消费运算符 token
        parser_state["pos"] += 1
        
        # 解析右操作数
        right_ast = _parse_additive(parser_state)
        
        # 构建 BINARY_OP AST
        return {
            "type": "BINARY_OP",
            "operator": op_value,
            "children": [left_ast, right_ast],
            "line": line,
            "column": column
        }
    
    # 没有比较运算符，返回左操作数
    return left_ast

# === helper functions ===

# === OOP compatibility layer ===
