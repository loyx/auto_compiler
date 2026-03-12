# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expr_package._parse_expr_src import _parse_expr
from ._parse_block_package._parse_block_src import _parse_block

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
def _parse_for_stmt(parser_state: ParserState) -> AST:
    """
    解析 for 语句。
    for_stmt := FOR IDENTIFIER IN expr COLON block
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. 消费 FOR token
    if pos >= len(tokens) or tokens[pos]["type"] != "FOR":
        parser_state["error"] = f"Expected FOR token at pos {pos}"
        return {"type": "ERROR", "line": 0, "column": 0}
    for_token = tokens[pos]
    pos += 1
    
    # 2. 消费 IDENTIFIER（循环变量）
    if pos >= len(tokens) or tokens[pos]["type"] != "IDENTIFIER":
        parser_state["error"] = f"Expected IDENTIFIER after FOR at pos {pos}"
        return {"type": "ERROR", "line": for_token["line"], "column": for_token["column"]}
    var_token = tokens[pos]
    pos += 1
    
    # 3. 消费 IN token
    if pos >= len(tokens) or tokens[pos]["type"] != "IN":
        parser_state["error"] = f"Expected IN token at pos {pos}"
        return {"type": "ERROR", "line": for_token["line"], "column": for_token["column"]}
    pos += 1
    
    # 4. 解析表达式
    expr_ast = _parse_expr(parser_state)
    pos = parser_state["pos"]
    
    # 5. 消费 COLON token
    if pos >= len(tokens) or tokens[pos]["type"] != "COLON":
        parser_state["error"] = f"Expected COLON token at pos {pos}"
        return {"type": "ERROR", "line": for_token["line"], "column": for_token["column"]}
    pos += 1
    
    # 6. 解析块
    block_ast = _parse_block(parser_state)
    pos = parser_state["pos"]
    
    # 7. 构建 FOR_STMT AST 节点
    parser_state["pos"] = pos
    return {
        "type": "FOR_STMT",
        "line": for_token["line"],
        "column": for_token["column"],
        "children": [
            {"type": "IDENTIFIER", "value": var_token["value"], "line": var_token["line"], "column": var_token["column"]},
            expr_ast,
            block_ast
        ]
    }

# === helper functions ===

# === OOP compatibility layer ===
