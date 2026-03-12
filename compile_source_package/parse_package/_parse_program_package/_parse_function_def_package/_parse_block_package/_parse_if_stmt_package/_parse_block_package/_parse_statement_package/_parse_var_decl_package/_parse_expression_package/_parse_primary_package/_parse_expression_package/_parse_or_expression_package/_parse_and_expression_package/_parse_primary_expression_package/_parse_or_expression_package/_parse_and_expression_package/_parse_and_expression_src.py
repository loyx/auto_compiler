# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_expression_package._parse_comparison_expression_src import _parse_comparison_expression

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
def _parse_and_expression(parser_state: ParserState) -> AST:
    """
    解析 AND 表达式（中等优先级）。
    输入 parser_state（原地修改），返回 AST 节点。
    会进一步调用 _parse_comparison_expression 处理比较运算。
    """
    # 1. 解析左侧 comparison expression
    left_ast = _parse_comparison_expression(parser_state)
    
    # 若已有错误，直接返回
    if parser_state.get("error"):
        return left_ast
    
    # 2. 循环检查 AND 运算符
    result_ast = left_ast
    while True:
        # 检查是否还有 token
        if parser_state["pos"] >= len(parser_state["tokens"]):
            break
        
        current_token = parser_state["tokens"][parser_state["pos"]]
        
        # 检查是否为 AND 运算符
        if current_token.get("value") != "AND":
            break
        
        # 3. 消费 AND token
        and_line = current_token.get("line", 0)
        and_column = current_token.get("column", 0)
        parser_state["pos"] += 1
        
        # 4. 解析右侧 comparison expression
        right_ast = _parse_comparison_expression(parser_state)
        
        # 若解析出错，返回已构建的 AST
        if parser_state.get("error"):
            return result_ast
        
        # 5. 构建二元运算 AST 节点
        result_ast = {
            "type": "binary_op",
            "operator": "and",
            "left": result_ast,
            "right": right_ast,
            "line": and_line,
            "column": and_column
        }
    
    return result_ast

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# Not needed for parser function nodes