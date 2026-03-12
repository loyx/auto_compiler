# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_expression_package._parse_additive_expression_src import _parse_additive_expression

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
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_comparison_expression(parser_state: ParserState) -> AST:
    """
    解析比较表达式（较高优先级）。
    处理 <, >, <=, >=, ==, != 等比较运算符。
    输入 parser_state（原地修改），返回 AST 节点。
    """
    left_ast = _parse_additive_expression(parser_state)
    
    if parser_state.get("error"):
        return left_ast
    
    result_ast = left_ast
    op_map = {"<": "lt", ">": "gt", "<=": "le", ">=": "ge", "==": "eq", "!=": "ne"}
    
    while True:
        if parser_state["pos"] >= len(parser_state["tokens"]):
            break
        
        current_token = parser_state["tokens"][parser_state["pos"]]
        token_value = current_token.get("value", "")
        
        if token_value not in ["<", ">", "<=", ">=", "==", "!="]:
            break
        
        op_line = current_token.get("line", 0)
        op_column = current_token.get("column", 0)
        parser_state["pos"] += 1
        
        right_ast = _parse_additive_expression(parser_state)
        
        if parser_state.get("error"):
            return result_ast
        
        result_ast = {
            "type": "binary_op",
            "operator": op_map[token_value],
            "left": result_ast,
            "right": right_ast,
            "line": op_line,
            "column": op_column
        }
    
    return result_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function
