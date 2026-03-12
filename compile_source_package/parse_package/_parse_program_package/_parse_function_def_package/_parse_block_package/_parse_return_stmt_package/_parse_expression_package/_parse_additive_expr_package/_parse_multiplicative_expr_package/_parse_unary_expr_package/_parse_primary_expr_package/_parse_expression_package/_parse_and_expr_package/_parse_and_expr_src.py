# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_expr_package._parse_comparison_expr_src import _parse_comparison_expr

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
def _parse_and_expr(parser_state: ParserState) -> AST:
    """
    解析 AND 层级表达式。
    
    处理 AND 运算符，调用 _parse_comparison_expr 解析操作数。
    原地修改 parser_state["pos"] 消费 token。
    """
    # 解析左侧表达式
    left_ast = _parse_comparison_expr(parser_state)
    
    # 循环处理 AND 运算符
    while _is_and_operator(parser_state):
        # 记录运算符位置
        current_token = parser_state["tokens"][parser_state["pos"]]
        op_line = current_token.get("line", 0)
        op_column = current_token.get("column", 0)
        
        # 消费运算符 token
        parser_state["pos"] += 1
        
        # 解析右侧表达式
        right_ast = _parse_comparison_expr(parser_state)
        
        # 构建 BINARY_OP 节点
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
def _is_and_operator(parser_state: ParserState) -> bool:
    """
    检查当前 token 是否为 AND 运算符。
    
    不修改 parser_state，仅做检查。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        return False
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    token_value = current_token.get("value", "")
    
    # 支持多种 AND 表示形式
    return token_type == "AND" or token_value.upper() == "AND" or token_value == "&&"

# === OOP compatibility layer ===
# Not required for this parser function node
