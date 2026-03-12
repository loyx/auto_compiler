# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_factor_package._parse_factor_src import _parse_factor

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,         # token 类型，如 "IDENT", "NUMBER", "MUL", "DIV", "LPAREN", "RPAREN"
#   "value": str,        # token 原始值
#   "line": int,         # 行号
#   "column": int        # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,         # 节点类型，如 "IDENT", "NUMBER", "BINOP"
#   "children": list,    # 子节点列表（BINOP 时使用）
#   "value": Any,        # 节点值（标识符名或数字值）
#   "operator": str,     # 运算符（BINOP 时使用，如 "*", "/"）
#   "line": int,         # 行号
#   "column": int        # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,      # Token 列表
#   "pos": int,          # 当前解析位置（索引）
#   "filename": str,     # 源文件名
#   "error": str         # 错误信息（可选）
# }


# === main function ===
def _parse_term(parser_state: ParserState) -> AST:
    """
    解析 term 层级语法：factor ((MUL | DIV) factor)*
    
    处理逻辑：
    1. 解析左侧 factor
    2. 循环检查是否有 MUL/DIV 运算符
    3. 如有运算符，消费运算符并解析右侧 factor
    4. 构建左结合的 BINOP AST 节点
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 解析左侧 factor
    left_ast = _parse_factor(parser_state)
    
    # 循环处理连续的 MUL/DIV 运算
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        if current_token["type"] not in ("MUL", "DIV"):
            break
        
        # 消费运算符
        op_token = tokens[parser_state["pos"]]
        parser_state["pos"] += 1
        
        # 解析右侧 factor
        right_ast = _parse_factor(parser_state)
        
        # 构建 BINOP 节点
        left_ast = {
            "type": "BINOP",
            "operator": "*" if op_token["type"] == "MUL" else "/",
            "children": [left_ast, right_ast],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left_ast


# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node