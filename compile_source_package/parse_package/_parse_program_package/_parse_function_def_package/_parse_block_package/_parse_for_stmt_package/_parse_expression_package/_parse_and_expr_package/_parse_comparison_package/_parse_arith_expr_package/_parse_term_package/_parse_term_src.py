# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_factor_package._parse_factor_src import _parse_factor

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (PLUS, MINUS, MULTI, DIV, MOD, LPAREN, RPAREN, IDENTIFIER, LITERAL, etc.)
#   "value": str,            # token 值 (+, -, *, /, %, (, ), 标识符名，字面量值等)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, ERROR, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值（运算符字符串或标识符/字面量值）
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
def _parse_term(parser_state: ParserState) -> AST:
    """
    解析 term 层级（乘除取模运算）。
    语法：term: factor ((MULTI | DIV | MOD) factor)*
    左结合构建 BINARY_OP 节点。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 解析左侧因子
    left = _parse_factor(parser_state)
    
    # 如果 factor 解析失败，直接返回 ERROR
    if left.get("type") == "ERROR":
        return left
    
    # 循环处理 MULTI/DIV/MOD 运算符
    while pos < len(tokens):
        token = tokens[pos]
        token_type = token.get("type", "")
        
        # 检查是否为乘除取模运算符
        if token_type not in ("MULTI", "DIV", "MOD"):
            break
        
        # 消耗运算符 token
        op_value = token.get("value", "")
        op_line = token.get("line", 0)
        op_column = token.get("column", 0)
        pos += 1
        
        # 解析右侧因子
        right = _parse_factor(parser_state)
        
        # 如果右侧 factor 解析失败，返回 ERROR
        if right.get("type") == "ERROR":
            return right
        
        # 构建 BINARY_OP 节点（左结合，使用左操作数的位置信息）
        left = {
            "type": "BINARY_OP",
            "value": op_value,
            "children": [left, right],
            "line": left.get("line", op_line),
            "column": left.get("column", op_column)
        }
    
    # 更新 parser_state 位置
    parser_state["pos"] = pos
    
    return left

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function nodes
