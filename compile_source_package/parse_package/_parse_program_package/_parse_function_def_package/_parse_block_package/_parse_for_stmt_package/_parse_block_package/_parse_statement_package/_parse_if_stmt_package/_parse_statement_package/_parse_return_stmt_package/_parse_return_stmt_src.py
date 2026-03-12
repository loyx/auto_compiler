# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._expect_token_package._expect_token_src import _expect_token
from ._parse_expression_package._parse_expression_src import _parse_expression

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
#   "type": str,             # RETURN_STMT
#   "children": list,        # [optional_expression_ast] 或空列表
#   "value": str,            # "return"
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
def _parse_return_stmt(parser_state: ParserState) -> AST:
    """
    解析 return 语句。
    语法：return [ expression ] ;
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 获取 RETURN token 信息用于 AST
    return_token = tokens[pos]
    line = return_token["line"]
    column = return_token["column"]
    
    # 1. 消耗 RETURN token
    parser_state = _expect_token(parser_state, "RETURN")
    
    # 2. 向前看：检查是否是 SEMICOLON（无返回值 return）
    children = []
    if parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        if current_token["type"] != "SEMICOLON":
            # 3. 解析返回表达式
            expr_ast = _parse_expression(parser_state)
            children.append(expr_ast)
    
    # 4. 消耗 SEMICOLON token
    parser_state = _expect_token(parser_state, "SEMICOLON")
    
    # 5. 构建 RETURN_STMT AST 节点
    ast_node: AST = {
        "type": "RETURN_STMT",
        "children": children,
        "value": "return",
        "line": line,
        "column": column
    }
    
    return ast_node

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node