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
def _parse_multiplicative_expression(parser_state: ParserState) -> AST:
    """
    解析乘法表达式（较高优先级）。
    处理 *, / 运算符，并会进一步调用 _parse_primary_expression。
    """
    # 解析左侧 primary expression
    left_ast = _parse_primary_expression(parser_state)
    
    # 检查错误
    if parser_state.get("error"):
        return left_ast
    
    # 循环处理乘法运算符
    while True:
        tokens = parser_state["tokens"]
        pos = parser_state["pos"]
        
        # 检查是否还有 token
        if pos >= len(tokens):
            break
        
        current_token = tokens[pos]
        token_value = current_token.get("value", "")
        token_type = current_token.get("type", "")
        
        # 检查是否为乘法运算符
        if token_value not in ("*", "/"):
            break
        
        # 保存运算符信息
        op_value = "mul" if token_value == "*" else "div"
        op_line = current_token.get("line", 0)
        op_column = current_token.get("column", 0)
        
        # 消费运算符 token
        parser_state["pos"] = pos + 1
        
        # 解析右侧 primary expression
        right_ast = _parse_primary_expression(parser_state)
        
        # 检查错误
        if parser_state.get("error"):
            # 返回已解析的部分 AST
            return left_ast
        
        # 构建二元运算 AST 节点
        left_ast = {
            "type": "binary_op",
            "operator": op_value,
            "left": left_ast,
            "right": right_ast,
            "line": op_line,
            "column": op_column
        }
    
    return left_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node
