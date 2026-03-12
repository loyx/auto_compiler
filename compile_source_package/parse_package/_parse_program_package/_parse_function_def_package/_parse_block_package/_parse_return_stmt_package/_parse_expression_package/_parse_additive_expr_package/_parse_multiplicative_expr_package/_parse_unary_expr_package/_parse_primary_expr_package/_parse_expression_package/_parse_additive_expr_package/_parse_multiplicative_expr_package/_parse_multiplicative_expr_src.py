# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
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
def _parse_multiplicative_expr(parser_state: ParserState) -> AST:
    """
    解析乘除法层级表达式（MULTIPLY, DIVIDE）。
    
    算法：
    1. 调用 _parse_unary_expr 解析左侧表达式
    2. 当当前 token 是乘除运算符时，循环处理右侧表达式
    3. 构建 BINARY_OP AST 节点
    4. 返回最终的 AST 节点
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 解析左侧表达式（unary level）
    left_ast = _parse_unary_expr(parser_state)
    
    # 循环处理乘除运算符
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        if current_token["type"] not in ("MULTIPLY", "DIVIDE"):
            break
        
        # 记录运算符位置
        op_line = current_token["line"]
        op_column = current_token["column"]
        
        # 映射运算符
        op_map = {
            "MULTIPLY": "*",
            "DIVIDE": "/"
        }
        operator = op_map[current_token["type"]]
        
        # 消费运算符 token
        parser_state["pos"] += 1
        
        # 解析右侧表达式（unary level）
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(
                f"Unexpected end of input after '{operator}' operator "
                f"at line {op_line}, column {op_column}"
            )
        
        right_ast = _parse_unary_expr(parser_state)
        
        # 构建 BINARY_OP AST 节点
        left_ast = {
            "type": "BINARY_OP",
            "operator": operator,
            "left": left_ast,
            "right": right_ast,
            "line": op_line,
            "column": op_column
        }
    
    return left_ast

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function nodes