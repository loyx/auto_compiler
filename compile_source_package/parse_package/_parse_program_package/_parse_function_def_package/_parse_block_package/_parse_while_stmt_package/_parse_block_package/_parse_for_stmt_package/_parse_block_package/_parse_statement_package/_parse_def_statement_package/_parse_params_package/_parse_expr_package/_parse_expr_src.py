# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_atom_package._parse_atom_src import _parse_atom

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
def _parse_expr(parser_state: ParserState) -> AST:
    """
    解析单个表达式（用于参数默认值）。
    支持：字面量、标识符、简单二元运算。
    副作用：更新 parser_state["pos"] 到表达式结束位置。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Incomplete expression")
    
    # 解析左操作数
    left_ast = _parse_atom(parser_state)
    
    # 检查是否有二元运算符
    pos = parser_state["pos"]
    if pos < len(tokens):
        current_token = tokens[pos]
        if current_token["type"] == "OP":
            op = current_token["value"]
            parser_state["pos"] = pos + 1
            
            # 解析右操作数
            right_ast = _parse_atom(parser_state)
            
            # 构建二元运算 AST
            return {
                "type": "BINOP",
                "op": op,
                "line": left_ast.get("line", current_token["line"]),
                "column": left_ast.get("column", current_token["column"]),
                "children": [left_ast, right_ast]
            }
    
    return left_ast

# === helper functions ===
# No helper functions

# === OOP compatibility layer ===
# Not needed for this parser function node
