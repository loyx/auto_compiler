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
#   "type": str,             # VAR_DECL
#   "children": list,        # [optional_init_expr_ast] 或空列表
#   "value": str,            # 变量名
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
def _parse_var_decl(parser_state: ParserState) -> AST:
    """
    解析变量声明语句。
    语法：var identifier [ = expression ] ;
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. 消耗 VAR token
    var_token = _expect_token(parser_state, "VAR")
    start_line = var_token["line"]
    start_column = var_token["column"]
    
    # 2. 消耗 IDENTIFIER token（变量名）
    id_token = _expect_token(parser_state, "IDENTIFIER")
    var_name = id_token["value"]
    
    # 3. 向前看：检查是否有初始化表达式
    children = []
    if parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        if current_token["type"] == "ASSIGN":
            # 3a. 消耗 ASSIGN token
            _expect_token(parser_state, "ASSIGN")
            # 3b. 解析初始化表达式
            init_expr = _parse_expression(parser_state)
            children.append(init_expr)
    
    # 5. 消耗 SEMICOLON token
    _expect_token(parser_state, "SEMICOLON")
    
    # 6. 构建 VAR_DECL AST 节点
    ast_node: AST = {
        "type": "VAR_DECL",
        "children": children,
        "value": var_name,
        "line": start_line,
        "column": start_column
    }
    
    return ast_node

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for parser function nodes