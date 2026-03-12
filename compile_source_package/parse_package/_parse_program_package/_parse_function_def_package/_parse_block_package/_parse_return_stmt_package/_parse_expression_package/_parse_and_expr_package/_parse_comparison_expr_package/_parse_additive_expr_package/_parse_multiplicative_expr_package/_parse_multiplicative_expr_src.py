# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (STAR, SLASH, IDENTIFIER, LITERAL, etc.)
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
def _parse_multiplicative_expr(parser_state: ParserState) -> AST:
    """
    解析乘法表达式（处理乘法/除法运算符：*, /）。
    
    算法：
    1. 调用 _parse_unary_expr 获取左操作数
    2. 循环检查当前 token 是否为乘法运算符类型（STAR, SLASH）
    3. 如果是，消费该 token，记录运算符，然后调用 _parse_unary_expr 获取右操作数
    4. 构建 BINARY_OP 节点，并将结果作为新的左操作数继续循环（左结合）
    5. 返回最终的 AST 节点
    """
    # 获取左操作数
    left = _parse_unary_expr(parser_state)
    
    # 循环处理乘法/除法运算符
    while _is_multiplicative_operator(parser_state):
        # 获取运算符 token
        op_token = _consume_current_token(parser_state)
        operator = op_token["value"]
        
        # 获取右操作数
        right = _parse_unary_expr(parser_state)
        
        # 构建二元运算节点
        left = _create_binary_op_node(left, right, operator, op_token)
    
    return left

# === helper functions ===
def _is_multiplicative_operator(parser_state: ParserState) -> bool:
    """检查当前 token 是否为乘法运算符（* 或 /）。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        return False
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    
    return token_type in ("STAR", "SLASH")

def _consume_current_token(parser_state: ParserState) -> Token:
    """消费当前 token 并推进位置指针。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        # 创建错误 token
        return {
            "type": "ERROR",
            "value": "",
            "line": 0,
            "column": 0
        }
    
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    
    return token

def _create_binary_op_node(left: AST, right: AST, operator: str, op_token: Token) -> AST:
    """创建二元运算 AST 节点。"""
    return {
        "type": "BINARY_OP",
        "children": [left, right],
        "value": operator,
        "line": op_token.get("line", 0),
        "column": op_token.get("column", 0)
    }

# === OOP compatibility layer ===
# Not needed for parser function nodes
