# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_expr_package._parse_multiplicative_expr_src import _parse_multiplicative_expr

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
def _parse_additive_expr(parser_state: ParserState) -> AST:
    """
    解析加法表达式（最低优先级的二元运算符表达式）。
    
    算法：
    1. 调用 _parse_multiplicative_expr 解析左侧操作数
    2. 检查当前 token 是否为加法运算符（"+" 或 "-"）
    3. 如果是，消费运算符并递归解析右侧操作数，构建 BINARY_OP 节点
    4. 如果不是，直接返回左侧操作数 AST
    5. 若出错则设置 parser_state["error"]
    """
    if parser_state.get("error"):
        return _create_error_ast(parser_state)
    
    # 解析左侧操作数（更高优先级的乘除表达式）
    left_ast = _parse_multiplicative_expr(parser_state)
    
    if parser_state.get("error"):
        return left_ast
    
    # 检查是否有加法运算符
    current_token = _get_current_token(parser_state)
    
    if current_token and current_token.get("value") in ("+", "-"):
        operator_token = current_token
        _consume_token(parser_state)
        
        # 解析右侧操作数
        right_ast = _parse_multiplicative_expr(parser_state)
        
        if parser_state.get("error"):
            return right_ast
        
        # 构建 BINARY_OP 节点
        return {
            "type": "BINARY_OP",
            "children": [left_ast, right_ast],
            "value": operator_token.get("value"),
            "line": operator_token.get("line"),
            "column": operator_token.get("column")
        }
    
    # 没有加法运算符，直接返回左侧操作数
    return left_ast


# === helper functions ===
def _get_current_token(parser_state: ParserState) -> Token:
    """获取当前位置的 token，如果超出范围则返回 None。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos < len(tokens):
        return tokens[pos]
    return None


def _consume_token(parser_state: ParserState) -> None:
    """消费当前 token，将 pos 向前移动一位。"""
    parser_state["pos"] = parser_state.get("pos", 0) + 1


def _create_error_ast(parser_state: ParserState) -> AST:
    """创建错误 AST 节点。"""
    return {
        "type": "ERROR",
        "children": [],
        "value": parser_state.get("error", "Unknown error"),
        "line": 0,
        "column": 0
    }

# === OOP compatibility layer ===
# Not needed for this parser function node