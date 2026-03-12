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
    解析 term 层级（乘除模运算，左结合）。
    语法：term: factor ((MULTI | DIV | MOD) factor)*
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否越界
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input in term"
        return {"type": "ERROR", "value": "Unexpected end of input", "children": [], "line": 0, "column": 0}
    
    # 解析第一个 factor
    left_ast = _parse_factor(parser_state)
    
    # 如果 factor 解析出错，直接返回
    if parser_state.get("error"):
        return left_ast
    
    # 循环处理乘除模运算符
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        token_type = current_token.get("type", "")
        
        # 检查是否为乘除模运算符
        if token_type not in ("MULTI", "DIV", "MOD"):
            break
        
        # 消耗运算符 token
        op_token = current_token
        parser_state["pos"] += 1
        
        # 解析右侧 factor
        right_ast = _parse_factor(parser_state)
        
        # 如果 factor 解析出错，返回错误
        if parser_state.get("error"):
            return right_ast
        
        # 构建二元运算节点（左结合）
        left_ast = {
            "type": "BINARY_OP",
            "value": op_token["value"],
            "children": [left_ast, right_ast],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
