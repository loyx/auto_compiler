# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_term_package._parse_term_src import _parse_term

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
def _parse_expression(parser_state: ParserState) -> AST:
    """
    解析表达式层级语法（处理加减运算符）。
    输入：parser_state（pos 指向表达式起始 token）
    输出：表达式的 AST 节点
    副作用：更新 parser_state['pos'] 到表达式结束位置
    错误：语法错误时抛 SyntaxError
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input at {parser_state.get('filename', 'unknown')}")
    
    # 1. 解析左侧项
    left_ast = _parse_term(parser_state)
    
    # 2. 循环处理加减运算符
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        if current_token["type"] not in ("PLUS", "MINUS"):
            break
        
        # 3. 消费运算符
        op_token = current_token
        parser_state["pos"] += 1
        
        # 4. 解析右侧项
        right_ast = _parse_term(parser_state)
        
        # 5. 构建二元运算 AST 节点
        left_ast = {
            "type": "BINOP",
            "operator": op_token["value"],
            "children": [left_ast, right_ast],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    # 6. 返回最终的 AST
    return left_ast

# === helper functions ===
# No helper functions needed - logic is delegated to _parse_term

# === OOP compatibility layer ===
# Not needed for parser function nodes