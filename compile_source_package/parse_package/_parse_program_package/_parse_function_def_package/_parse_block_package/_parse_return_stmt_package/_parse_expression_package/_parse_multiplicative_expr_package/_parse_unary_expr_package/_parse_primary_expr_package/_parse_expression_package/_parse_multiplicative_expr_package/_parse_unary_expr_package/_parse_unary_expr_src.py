# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr

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
def _parse_unary_expr(parser_state: ParserState) -> AST:
    """
    解析一元表达式（unary expressions），处理前缀运算符如 +, -, not, ! 等。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否还有 token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input while parsing unary expression")
    
    current_token = tokens[pos]
    
    # 检查是否为一元运算符
    UNARY_OPERATORS = {"+", "-", "not", "!", "~"}
    
    if current_token.get("type") == "OPERATOR" and current_token.get("value") in UNARY_OPERATORS:
        # 消费运算符 token
        op_token = tokens[pos]
        parser_state["pos"] += 1
        
        # 递归解析操作数（允许链式一元运算符，如 --x, !!!flag）
        operand = _parse_unary_expr(parser_state)
        
        # 构建 UNARY_OP 节点
        return {
            "type": "UNARY_OP",
            "operator": op_token["value"],
            "children": [operand],
            "line": op_token.get("line", 0),
            "column": op_token.get("column", 0)
        }
    else:
        # 不是一元运算符，解析 primary expression
        return _parse_primary_expr(parser_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node