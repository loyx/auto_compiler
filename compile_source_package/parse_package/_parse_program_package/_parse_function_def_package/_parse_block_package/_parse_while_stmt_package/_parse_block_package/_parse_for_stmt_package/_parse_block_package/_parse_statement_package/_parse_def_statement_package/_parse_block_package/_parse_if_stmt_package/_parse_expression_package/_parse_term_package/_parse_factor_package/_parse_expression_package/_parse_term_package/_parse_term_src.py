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
#   "operator": str,
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
def _parse_term(parser_state: ParserState) -> AST:
    """
    解析项层级语法（处理乘除运算符和原子值）。
    输入：parser_state（pos 指向项起始 token）
    输出：项的 AST 节点
    副作用：更新 parser_state['pos'] 到项结束位置
    错误：语法错误时抛 SyntaxError
    """
    # 步骤 1: 解析左侧原子值
    left_ast = _parse_atom(parser_state)
    
    # 步骤 2: 循环处理乘除运算符
    while True:
        tokens = parser_state["tokens"]
        pos = parser_state["pos"]
        
        # 检查是否还有 token
        if pos >= len(tokens):
            break
        
        current_token = tokens[pos]
        
        # 检查是否为乘除运算符
        if current_token["type"] not in ("MULTIPLY", "DIVIDE"):
            break
        
        # 步骤 3: 消费运算符
        operator = "*" if current_token["type"] == "MULTIPLY" else "/"
        op_line = current_token["line"]
        op_column = current_token["column"]
        parser_state["pos"] = pos + 1
        
        # 步骤 4: 解析右侧原子值
        right_ast = _parse_atom(parser_state)
        
        # 步骤 5: 构建二元运算 AST 节点
        left_ast = {
            "type": "BINOP",
            "operator": operator,
            "children": [left_ast, right_ast],
            "line": op_line,
            "column": op_column
        }
    
    # 步骤 6: 返回最终的 AST
    return left_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node
