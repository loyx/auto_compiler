# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (AND, OR, NOT, IDENTIFIER, LITERAL, etc.)
#   "value": str,            # token 值（源代码中的实际字符）
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, etc.)
#   "operator": str,         # 运算符 (仅 BINARY_OP/UNARY_OP)
#   "left": AST,             # 左操作数 (仅 BINARY_OP)
#   "right": AST,            # 右操作数 (仅 BINARY_OP)
#   "operand": AST,          # 操作数 (仅 UNARY_OP)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }

# === main function ===
def _parse_unary_expr(parser_state: ParserState) -> AST:
    """解析一元表达式（最高优先级）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否还有 token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input while parsing unary expression")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    # 一元运算符映射
    unary_operators = {
        "NOT": "!",
        "MINUS": "-"
    }
    
    # 检查是否为一元运算符
    if token_type in unary_operators:
        operator = unary_operators[token_type]
        line = current_token["line"]
        column = current_token["column"]
        
        # 消费运算符 token
        parser_state["pos"] += 1
        
        # 递归解析操作数
        operand = _parse_unary_expr(parser_state)
        
        # 构建 UNARY_OP AST 节点
        return {
            "type": "UNARY_OP",
            "operator": operator,
            "operand": operand,
            "line": line,
            "column": column
        }
    else:
        # 解析原子表达式
        return _parse_primary_expr(parser_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function
