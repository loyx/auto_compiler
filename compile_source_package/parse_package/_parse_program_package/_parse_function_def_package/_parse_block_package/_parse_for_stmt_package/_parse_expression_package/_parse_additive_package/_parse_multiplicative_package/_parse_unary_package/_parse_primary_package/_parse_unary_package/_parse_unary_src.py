# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary

# Re-export for testing purposes (allows patching at this module level)
__all__ = ['_parse_unary', '_parse_primary']

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
def _parse_unary(parser_state: ParserState) -> AST:
    """
    解析一元表达式（unary expression）。
    
    处理一元运算符（MINUS, NOT, PLUS）或基础表达式。
    一元运算符是右结合的，例如 --x 解析为 -(-x)。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 边界检查：tokens 为空或 pos 越界
    if not tokens or pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input while parsing unary expression"
        return _create_error_node(parser_state, "Unexpected end of input")
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    token_value = current_token.get("value", "")
    token_line = current_token.get("line", 0)
    token_column = current_token.get("column", 0)
    
    # 检查是否为一元运算符
    unary_operators = {"MINUS", "NOT", "PLUS"}
    
    if token_type in unary_operators:
        # 消费运算符 token
        parser_state["pos"] = pos + 1
        
        # 递归解析操作数（右结合）
        operand_ast = _parse_unary(parser_state)
        
        # 检查递归解析是否出错
        if parser_state.get("error"):
            return operand_ast
        
        # 构建 UNARY_OP 节点
        return {
            "type": "UNARY_OP",
            "value": token_value,
            "children": [operand_ast],
            "line": token_line,
            "column": token_column
        }
    else:
        # 不是运算符，解析基础表达式
        return _parse_primary(parser_state)

# === helper functions ===
def _create_error_node(parser_state: ParserState, error_message: str) -> AST:
    """创建错误 AST 节点。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 获取当前位置的行号和列号
    line = 0
    column = 0
    if tokens and pos < len(tokens):
        line = tokens[pos].get("line", 0)
        column = tokens[pos].get("column", 0)
    
    return {
        "type": "ERROR",
        "value": error_message,
        "children": [],
        "line": line,
        "column": column
    }

# === OOP compatibility layer ===
# Not required for this parser utility function
