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
def _parse_not_expr(parser_state: ParserState) -> AST:
    """
    解析 'not' 表达式（较高优先级）。
    
    语法：'not' not_expr | primary_expr
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否越界
    if pos >= len(tokens):
        return _parse_primary_expr(parser_state)
    
    current_token = tokens[pos]
    
    # 检查当前 token 是否为 "NOT" 类型
    if current_token.get("type") == "NOT":
        # 记录 not 关键字的位置
        not_line = current_token.get("line", 0)
        not_column = current_token.get("column", 0)
        
        # 消费 NOT token
        parser_state["pos"] = pos + 1
        
        # 递归调用解析操作数
        operand = _parse_not_expr(parser_state)
        
        # 构建 UNARY_OP 节点
        return {
            "type": "UNARY_OP",
            "value": "not",
            "children": [operand],
            "line": not_line,
            "column": not_column
        }
    else:
        # 不是 NOT，解析 primary 表达式
        return _parse_primary_expr(parser_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function