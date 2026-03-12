# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_term_package._parse_term_src import _parse_term

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
def _parse_arith_expr(parser_state: ParserState) -> AST:
    """
    解析算术表达式（加减层级）。
    语法：arith_expr: term ((PLUS | MINUS) term)*
    左结合构建 AST。
    """
    tokens = parser_state.get("tokens", [])
    
    # 解析左侧 term
    left = _parse_term(parser_state)
    if left.get("type") == "ERROR":
        return left
    
    # 循环处理 PLUS/MINUS 运算符
    while parser_state.get("pos", 0) < len(tokens):
        token = tokens[parser_state["pos"]]
        token_type = token.get("type", "")
        
        if token_type not in ("PLUS", "MINUS"):
            break
        
        op_token = token
        parser_state["pos"] += 1
        
        # 解析右侧 term
        right = _parse_term(parser_state)
        if right.get("type") == "ERROR":
            return right
        
        # 构建 BINARY_OP 节点（左结合）
        left = {
            "type": "BINARY_OP",
            "value": op_token.get("value", ""),
            "children": [left, right],
            "line": left.get("line", op_token.get("line", 0)),
            "column": left.get("column", op_token.get("column", 0))
        }
    
    return left

# === helper functions ===

# === OOP compatibility layer ===
