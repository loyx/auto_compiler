# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,        # token 类型，如 "NUMBER", "IDENTIFIER", "LPAREN", "PLUS" 等
#   "value": str,       # token 原始值
#   "line": int,        # 行号
#   "column": int       # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,        # 节点类型，如 "BinaryOp", "UnaryOp", "Literal", "Identifier"
#   "children": list,   # 子节点列表（对于运算节点）
#   "value": Any,       # 节点值（对于字面量或标识符）
#   "line": int,        # 行号
#   "column": int       # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,     # Token 列表
#   "pos": int,         # 当前解析位置（索引）
#   "filename": str,    # 源文件名
#   "error": str        # 错误信息（可选）
# }

# === main function ===
def _parse_expression(parser_state: ParserState) -> AST:
    """
    解析完整表达式。
    
    这是表达式解析的入口函数，处理：
    1. 调用 _parse_primary_expr 获取左侧操作数
    2. 根据后续 token 判断是否存在运算符
    3. 如果存在运算符，继续解析右侧操作数并构建二元运算 AST
    4. 返回完整的表达式 AST
    """
    # 获取左侧操作数（初级表达式）
    left = _parse_primary_expr(parser_state)
    
    # 检查是否有后续运算符
    while _has_operator(parser_state):
        op_token = _get_current_token(parser_state)
        parser_state["pos"] += 1  # 消费运算符 token
        
        # 获取右侧操作数
        right = _parse_primary_expr(parser_state)
        
        # 构建二元运算 AST 节点
        left = _build_binary_op_ast(op_token, left, right)
    
    return left

# === helper functions ===
def _has_operator(parser_state: ParserState) -> bool:
    """检查当前 token 是否为运算符。"""
    token = _get_current_token(parser_state)
    if token is None:
        return False
    
    operator_types = {"PLUS", "MINUS", "STAR", "SLASH", "PERCENT", 
                      "EQ", "NE", "LT", "LE", "GT", "GE",
                      "AND", "OR"}
    return token.get("type") in operator_types

def _get_current_token(parser_state: ParserState) -> Token:
    """获取当前 token，如果超出范围则返回 None。"""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    if pos < len(tokens):
        return tokens[pos]
    return None

def _build_binary_op_ast(op_token: Token, left: AST, right: AST) -> AST:
    """构建二元运算 AST 节点。"""
    return {
        "type": "BinaryOp",
        "operator": op_token.get("value"),
        "left": left,
        "right": right,
        "line": op_token.get("line", 0),
        "column": op_token.get("column", 0)
    }

# === OOP compatibility layer ===
# Not required for this parser function node
