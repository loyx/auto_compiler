# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
from ._parse_term_package._parse_term_src import _parse_term

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
#   "column": int,
#   "operator": str,
#   "left": AST,
#   "right": AST
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": List[Token],
#   "pos": int,
#   "filename": str,
#   "error": str
# }

ComparisonOperators = List[str]
# ComparisonOperators possible values:
# ["<", "<=", ">", ">="]

# === main function ===
def _parse_comparison(parser_state: ParserState) -> AST:
    """
    解析 comparison 层级表达式。
    语法：comparison := term ( ( "<" | "<=" | ">" | ">=" ) term )*
    """
    comparison_ops: ComparisonOperators = ["<", "<=", ">", ">="]
    
    # 解析左侧第一个 term
    left_ast = _parse_term(parser_state)
    
    # 如果解析 term 时出错，直接返回
    if parser_state.get("error"):
        return left_ast
    
    # 循环处理后续的比较运算符
    while True:
        pos = parser_state["pos"]
        tokens = parser_state["tokens"]
        
        # 检查是否还有 token
        if pos >= len(tokens):
            break
        
        current_token = tokens[pos]
        token_value = current_token.get("value", "")
        
        # 检查是否是关系运算符
        if token_value not in comparison_ops:
            break
        
        # 记录运算符和位置信息
        operator = token_value
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        
        # 前进 pos，越过运算符
        parser_state["pos"] = pos + 1
        
        # 解析右侧 term
        right_ast = _parse_term(parser_state)
        
        # 如果解析 term 时出错，直接返回
        if parser_state.get("error"):
            return left_ast
        
        # 构建 Binary AST 节点
        left_ast = {
            "type": "Binary",
            "operator": operator,
            "left": left_ast,
            "right": right_ast,
            "line": line,
            "column": column
        }
    
    return left_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function