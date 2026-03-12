# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
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
def _parse_for_stmt(parser_state: dict) -> dict:
    """解析 for 循环语句：for (init; cond; update) { ... }"""
    tokens = parser_state["tokens"]
    filename = parser_state["filename"]
    
    # 1. 记录 FOR 关键字位置
    if parser_state["pos"] >= len(tokens):
        line, column = 0, 0
    else:
        for_token = tokens[parser_state["pos"]]
        line, column = for_token["line"], for_token["column"]
    
    # 2. 消费 FOR
    _consume_token(parser_state, "FOR")
    
    # 3. 消费 LPAREN
    _consume_token(parser_state, "LPAREN")
    
    # 4. 解析初始化部分
    init_ast = _parse_optional_expression(parser_state, tokens, filename, "SEMICOLON")
    
    # 5. 消费 SEMICOLON
    _consume_token(parser_state, "SEMICOLON")
    
    # 6. 解析条件部分
    cond_ast = _parse_optional_expression(parser_state, tokens, filename, "SEMICOLON")
    
    # 7. 消费 SEMICOLON
    _consume_token(parser_state, "SEMICOLON")
    
    # 8. 解析更新部分
    update_ast = _parse_optional_expression(parser_state, tokens, filename, "RPAREN")
    
    # 9. 消费 RPAREN
    _consume_token(parser_state, "RPAREN")
    
    # 10. 解析循环体块
    body_ast = _parse_block(parser_state)
    
    # 11. 构建 FOR_STMT AST 节点
    return {
        "type": "FOR_STMT",
        "children": [init_ast, cond_ast, update_ast, body_ast],
        "line": line,
        "column": column
    }

# === helper functions ===
def _consume_token(parser_state: dict, expected_type: str) -> None:
    """消费一个期望类型的 token，若不匹配则抛出 SyntaxError。"""
    tokens = parser_state["tokens"]
    filename = parser_state["filename"]
    
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of file, expected '{expected_type}'")
    
    current_token = tokens[parser_state["pos"]]
    if current_token["type"] != expected_type:
        raise SyntaxError(
            f"{filename}:{current_token['line']}:{current_token['column']}: "
            f"Expected '{expected_type}', found '{current_token['type']}'"
        )
    
    parser_state["pos"] += 1

def _parse_optional_expression(
    parser_state: dict, 
    tokens: list, 
    filename: str, 
    terminator_type: str
) -> dict:
    """解析可选表达式：如果下一个 token 是终止符则返回 None，否则调用 _parse_expression。"""
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of file")
    
    next_token = tokens[parser_state["pos"]]
    if next_token["type"] == terminator_type:
        return None
    
    return _parse_expression(parser_state)

# === OOP compatibility layer ===
