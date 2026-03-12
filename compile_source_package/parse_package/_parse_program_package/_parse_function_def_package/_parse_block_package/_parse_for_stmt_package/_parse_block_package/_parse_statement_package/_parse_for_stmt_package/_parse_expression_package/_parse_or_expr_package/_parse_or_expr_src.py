# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_expr_package._parse_and_expr_src import _parse_and_expr
from ._current_token_package._current_token_src import _current_token
from ._advance_package._advance_src import _advance

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
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL)
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
    """
    解析 or 表达式（最低优先级）。
    使用递归下降解析，处理左结合的 or 运算。
    """
    # 1. 解析左侧 and 表达式
    left_ast = _parse_and_expr(parser_state)
    
    # 2. 循环处理 or 运算符
    while True:
        current = _current_token(parser_state)
        
        # 3. 检查是否为 "or" 运算符
        if current.get("type") != "OR":
            break
        
        # 4. 消耗 or token
        _advance(parser_state)
        
        # 5. 解析右侧 and 表达式
        right_ast = _parse_and_expr(parser_state)
        
        # 6. 构建 BINARY_OP 节点
        left_ast = {
            "type": "BINARY_OP",
            "value": "or",
            "children": [left_ast, right_ast],
            "line": current.get("line", 0),
            "column": current.get("column", 0)
        }
    
    return left_ast

# === helper functions ===
# No helper functions needed - logic is in main function

# === OOP compatibility layer ===
# Not needed - this is a parser utility function, not a framework entry point