# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr

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
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, PAREN_EXPR, ERROR, etc.)
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
    """解析一元表达式。
    
    处理 MINUS、PLUS、NOT、BITWISE_NOT 等一元运算符，返回 UNARY_OP 节点。
    非一元运算符时委托给 _parse_primary_expr 处理。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 检查是否还有 token
    if pos >= len(tokens):
        return _create_error_node(parser_state, "Unexpected end of input")
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    
    # 一元运算符集合
    unary_operators = {"MINUS", "PLUS", "NOT", "BITWISE_NOT"}
    
    if token_type in unary_operators:
        # 消费一元运算符 token
        operator_token = tokens[parser_state["pos"]]
        parser_state["pos"] += 1
        
        # 递归解析操作数（支持链式一元运算如 --x）
        operand_ast = _parse_unary_expr(parser_state)
        
        # 检查操作数解析是否出错
        if parser_state.get("error"):
            return operand_ast  # 错误已由下层设置
        
        # 创建 UNARY_OP 节点
        return {
            "type": "UNARY_OP",
            "children": [operand_ast],
            "value": operator_token.get("type"),
            "line": operator_token.get("line", 0),
            "column": operator_token.get("column", 0)
        }
    else:
        # 非一元运算符，委托给 _parse_primary_expr
        return _parse_primary_expr(parser_state)

# === helper functions ===
def _create_error_node(parser_state: ParserState, message: str) -> AST:
    """创建 ERROR 类型的 AST 节点并设置 parser_state['error']。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 设置错误信息
    parser_state["error"] = message
    
    # 获取错误位置
    if pos < len(tokens):
        token = tokens[pos]
        line = token.get("line", 0)
        column = token.get("column", 0)
    else:
        line = 0
        column = 0
    
    return {
        "type": "ERROR",
        "children": [],
        "value": message,
        "line": line,
        "column": column
    }

# === OOP compatibility layer ===
# Not required for this function node (parser helper function)
