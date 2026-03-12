# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_package._parse_and_src import _parse_and
from ._consume_token_package._consume_token_src import _consume_token

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
#   "op": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
#   "callee": AST,
#   "args": list,
#   "line": int,
#   "column": int
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
def _parse_or(parser_state: ParserState) -> AST:
    """
    解析 OR 表达式（优先级 Level 1，最低）。
    左结合：a || b || c 解析为 ((a || b) || c)
    """
    # 解析左侧操作数（调用更高优先级的 _parse_and）
    left_ast = _parse_and(parser_state)
    
    # 检查是否有错误
    if parser_state.get("error"):
        return left_ast
    
    # 循环处理 || 运算符（左结合）
    while True:
        # 检查当前 token 是否为 OR 类型
        tokens = parser_state.get("tokens", [])
        pos = parser_state.get("pos", 0)
        
        if pos >= len(tokens):
            break
        
        current_token = tokens[pos]
        if current_token.get("type") != "OR":
            break
        
        # 记录位置信息用于 AST 节点
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        
        # 消费 OR token
        _consume_token(parser_state, "OR")
        
        # 检查消费后是否有错误
        if parser_state.get("error"):
            return left_ast
        
        # 解析右侧操作数
        right_ast = _parse_and(parser_state)
        
        # 检查是否有错误
        if parser_state.get("error"):
            return left_ast
        
        # 构建 BINARY_OP 节点（左结合）
        left_ast = {
            "type": "BINARY_OP",
            "op": "||",
            "left": left_ast,
            "right": right_ast,
            "line": line,
            "column": column
        }
    
    return left_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
