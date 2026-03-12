# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_expr_package._parse_and_expr_src import _parse_and_expr

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
def _parse_or_expr(parser_state: ParserState) -> AST:
    """解析 OR 层级表达式（最低优先级）。"""
    # 解析左侧表达式
    left = _parse_and_expr(parser_state)
    
    # 循环处理 OR 运算符
    while _is_current_token(parser_state, "OR"):
        # 记录运算符位置
        op_token = _get_current_token(parser_state)
        line = op_token["line"]
        column = op_token["column"]
        
        # 消费运算符 token
        _consume_token(parser_state)
        
        # 解析右侧表达式
        right = _parse_and_expr(parser_state)
        
        # 构建 BINARY_OP AST 节点
        left = {
            "type": "BINARY_OP",
            "operator": "||",
            "left": left,
            "right": right,
            "line": line,
            "column": column
        }
    
    return left

# === helper functions ===
def _is_current_token(parser_state: ParserState, token_type: str) -> bool:
    """检查当前 token 是否为指定类型。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        return False
    return tokens[pos]["type"] == token_type

def _get_current_token(parser_state: ParserState) -> Token:
    """获取当前 token。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input in {parser_state.get('filename', 'unknown')}")
    return tokens[pos]

def _consume_token(parser_state: ParserState) -> None:
    """消费当前 token（前进 pos）。"""
    parser_state["pos"] += 1

# === OOP compatibility layer ===
# Not needed for parser function node
