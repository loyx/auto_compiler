# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_atom_expr_package._parse_atom_expr_src import _parse_atom_expr

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
    解析 NOT 表达式（高优先级）。
    
    如果当前位置是 NOT 运算符，构建 UNARY_OP 节点；
    否则解析原子表达式。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否越界
    if pos >= len(tokens):
        return _parse_atom_expr(parser_state)
    
    current_token = tokens[pos]
    
    # 检查是否为 NOT 运算符
    if current_token.get("type") == "NOT":
        # 记录 NOT token 的位置信息
        not_line = current_token.get("line", 0)
        not_column = current_token.get("column", 0)
        
        # 消费 NOT token
        parser_state["pos"] = pos + 1
        
        # 递归解析被否定的表达式
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
        # 不是 NOT，解析原子表达式
        return _parse_atom_expr(parser_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function