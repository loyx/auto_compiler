# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr

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
def _parse_and_expr(parser_state: ParserState) -> AST:
    """
    解析 AND 层级表达式（中等优先级）。
    
    处理连续的 AND 运算符，构建左结合的 BINARY_OP AST 节点。
    算法：先解析左侧一元表达式，然后循环处理 AND 运算符。
    """
    # 解析左侧表达式
    left_ast = _parse_unary_expr(parser_state)
    
    # 循环处理连续的 AND 运算符
    while _is_current_token(parser_state, "AND"):
        # 记录运算符位置
        op_token = _get_current_token(parser_state)
        op_line = op_token["line"]
        op_column = op_token["column"]
        
        # 消费 AND 运算符
        _consume_token(parser_state)
        
        # 解析右侧表达式
        right_ast = _parse_unary_expr(parser_state)
        
        # 构建 BINARY_OP AST 节点
        left_ast = {
            "type": "BINARY_OP",
            "operator": "&&",
            "left": left_ast,
            "right": right_ast,
            "line": op_line,
            "column": op_column
        }
    
    return left_ast


# === helper functions ===
def _get_current_token(parser_state: ParserState) -> Token:
    """
    获取当前 token。
    
    如果当前位置超出 tokens 列表边界，抛出 SyntaxError。
    """
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input in {parser_state.get('filename', 'unknown')}")
    return tokens[pos]


def _is_current_token(parser_state: ParserState, token_type: str) -> bool:
    """
    检查当前 token 是否为指定类型。
    
    如果当前位置超出边界，返回 False。
    """
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        return False
    return tokens[pos]["type"] == token_type


def _consume_token(parser_state: ParserState) -> None:
    """
    消费当前 token（前进 pos 指针）。
    
    原地修改 parser_state["pos"]。
    """
    parser_state["pos"] += 1


# === OOP compatibility layer ===
# 本模块为普通函数节点，无需 OOP wrapper
