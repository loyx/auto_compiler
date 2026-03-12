# === std / third-party imports ===
from typing import Any, Dict, List

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
    解析 expression 层级（加减运算，最低优先级）。
    语法：expression: term ((PLUS | MINUS) term)*
    """
    tokens: List[Token] = parser_state["tokens"]
    pos: int = parser_state["pos"]
    
    # 解析左侧 term
    left_ast = _parse_term(parser_state)
    
    # 如果 term 解析出错，直接返回
    if parser_state.get("error"):
        return left_ast
    
    # 循环处理 PLUS/MINUS 运算符
    while pos < len(tokens):
        current_token = tokens[pos]
        token_type = current_token.get("type", "")
        
        if token_type not in ("PLUS", "MINUS"):
            break
        
        # 消耗运算符 token
        op_token = tokens[pos]
        pos += 1
        
        # 解析右侧 term
        parser_state["pos"] = pos
        right_ast = _parse_term(parser_state)
        
        # 如果 term 解析出错，直接返回
        if parser_state.get("error"):
            return right_ast
        
        # 构建 BINARY_OP 节点
        left_ast = {
            "type": "BINARY_OP",
            "value": op_token["value"],
            "children": [left_ast, right_ast],
            "line": op_token["line"],
            "column": op_token["column"]
        }
        
        # 更新位置
        pos = parser_state["pos"]
    
    parser_state["pos"] = pos
    return left_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function