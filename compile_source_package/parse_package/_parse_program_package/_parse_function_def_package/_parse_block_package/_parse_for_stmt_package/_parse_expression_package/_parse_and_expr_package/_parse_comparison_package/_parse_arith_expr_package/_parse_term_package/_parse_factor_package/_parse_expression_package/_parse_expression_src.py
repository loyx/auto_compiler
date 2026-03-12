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
def _parse_expression(parser_state: ParserState) -> AST:
    """
    解析 expression 层级（加减运算，左结合）。
    语法：expression: term ((PLUS | MINUS) term)*
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 解析第一个 term
    left = _parse_term(parser_state)
    
    # 检查是否有错误
    if parser_state.get("error"):
        return left
    
    # 循环处理 PLUS/MINUS 运算符
    while pos < len(tokens):
        token = tokens[pos]
        token_type = token.get("type", "")
        
        if token_type not in ("PLUS", "MINUS"):
            break
        
        # 消耗运算符 token
        op_token = token
        parser_state["pos"] = pos + 1
        pos = pos + 1
        
        # 解析右侧 term
        right = _parse_term(parser_state)
        
        # 检查是否有错误
        if parser_state.get("error"):
            return right
        
        # 构建 BINARY_OP 节点（左结合）
        left = {
            "type": "BINARY_OP",
            "value": op_token["value"],
            "children": [left, right],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for parser internal function