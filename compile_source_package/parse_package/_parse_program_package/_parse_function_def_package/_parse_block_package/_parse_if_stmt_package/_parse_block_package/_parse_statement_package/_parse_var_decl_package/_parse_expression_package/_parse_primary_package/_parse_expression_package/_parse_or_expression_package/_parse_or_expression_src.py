# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_expression_package._parse_and_expression_src import _parse_and_expression
from ._consume_token_package._consume_token_src import _consume_token
from ._make_binary_op_package._make_binary_op_src import _make_binary_op

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "line": int,
#   "column": int,
#   "operator": str,
#   "left": AST,
#   "right": AST
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_or_expression(parser_state: ParserState) -> AST:
    """
    解析 OR 表达式（最低优先级）。
    递归下降解析的第一层，处理左结合的 OR 运算符。
    """
    # 1. 解析左侧的 AND 表达式
    left_ast = _parse_and_expression(parser_state)
    
    # 检查是否有错误
    if parser_state.get("error"):
        return left_ast
    
    # 2. 循环处理 OR 运算符（左结合）
    while _current_token_is_or(parser_state):
        # 记录 OR token 的位置信息
        or_token = _peek_token(parser_state)
        line = or_token.get("line", 0)
        column = or_token.get("column", 0)
        
        # 3. 消费 OR token
        _consume_token(parser_state, "OR")
        
        # 检查是否有错误
        if parser_state.get("error"):
            return left_ast
        
        # 4. 解析右侧的 AND 表达式
        right_ast = _parse_and_expression(parser_state)
        
        # 检查是否有错误
        if parser_state.get("error"):
            return left_ast
        
        # 5. 构建 binary_op AST 节点
        left_ast = _make_binary_op("or", left_ast, right_ast, line, column)
    
    # 6. 返回最终的 AST 节点
    return left_ast

# === helper functions ===
def _current_token_is_or(parser_state: ParserState) -> bool:
    """检查当前 token 是否为 OR 运算符。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        return False
    
    current_token = tokens[pos]
    return current_token.get("type") == "OR"

def _peek_token(parser_state: ParserState) -> Token:
    """查看当前 token（不消费）。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        return {"type": "EOF", "value": "", "line": 0, "column": 0}
    
    return tokens[pos]

# === OOP compatibility layer ===
# Not required for this parser function node
