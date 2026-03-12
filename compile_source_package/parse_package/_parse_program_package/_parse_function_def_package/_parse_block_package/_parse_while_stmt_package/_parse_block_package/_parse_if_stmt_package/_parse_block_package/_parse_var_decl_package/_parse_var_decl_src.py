# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# only import child functions
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_expr_package._parse_expr_src import _parse_expr

# === ADT defines ===
# define the data structures used between parent and child functions
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
def _parse_var_decl(parser_state: dict) -> dict:
    """解析变量声明语句。输入：parser_state（pos 指向 VAR/LET/CONST token）。
    返回 VAR_DECL 类型 AST 节点。函数内部会更新 parser_state 的位置。"""
    # 1. 消费 VAR/LET/CONST token，记录声明类型
    decl_token = _consume_token(parser_state)
    decl_type = decl_token["type"]  # "VAR", "LET", or "CONST"
    
    # 验证 token 类型
    if decl_type not in ("VAR", "LET", "CONST"):
        raise SyntaxError(f"Expected variable declaration keyword, got {decl_type}")
    
    # 2. 解析变量名标识符
    ident_token = _consume_token(parser_state, "IDENTIFIER")
    identifier_ast = {
        "type": "IDENTIFIER",
        "value": ident_token["value"],
        "line": ident_token["line"],
        "column": ident_token["column"]
    }
    
    # 3. 检查是否有赋值符号，如果有则解析表达式
    expr_ast = None
    if parser_state["pos"] < len(parser_state["tokens"]):
        next_token = parser_state["tokens"][parser_state["pos"]]
        if next_token["type"] == "ASSIGN":
            # 消费 ASSIGN token
            _consume_token(parser_state, "ASSIGN")
            # 解析表达式
            expr_ast = _parse_expr(parser_state)
    
    # 4. 消费分号
    _consume_token(parser_state, "SEMICOLON")
    
    # 5. 返回 VAR_DECL 节点
    return {
        "type": "VAR_DECL",
        "children": [identifier_ast, expr_ast] if expr_ast is not None else [identifier_ast],
        "line": decl_token["line"],
        "column": decl_token["column"]
    }

# === helper functions ===
# 本函数逻辑清晰，无需额外 helper 函数

# === OOP compatibility layer ===
# 本函数为解析器内部函数，不需要 OOP wrapper