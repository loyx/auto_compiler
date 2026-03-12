# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (IDENTIFIER, NUMBER, STRING, LPAREN, RPAREN, OPERATOR, etc.)
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (UNARY_OP, IDENTIFIER, LITERAL, ERROR, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值（operator 符号或字面量值）
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息
# }

UNARY_OPERATORS = {"-", "+", "!", "~"}


# === main function ===
def _parse_unary_expr(parser_state: ParserState) -> AST:
    """解析一元表达式（包括一元运算符和基本表达式）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否已到 tokens 末尾
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input while parsing unary expression"
        return {"type": "ERROR", "children": [], "value": None, "line": -1, "column": -1}
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    token_value = current_token.get("value", "")
    token_line = current_token.get("line", -1)
    token_column = current_token.get("column", -1)
    
    # 检查是否为一元运算符
    if token_type == "OPERATOR" and token_value in UNARY_OPERATORS:
        # 消费运算符 token
        parser_state["pos"] = pos + 1
        
        # 递归解析操作数
        operand_ast = _parse_unary_expr(parser_state)
        
        # 如果递归解析出错，直接返回错误
        if parser_state.get("error"):
            return operand_ast
        
        # 创建 UNARY_OP 节点
        return {
            "type": "UNARY_OP",
            "children": [operand_ast],
            "value": token_value,
            "line": token_line,
            "column": token_column
        }
    else:
        # 解析基本表达式
        return _parse_primary_expr(parser_state)


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function
