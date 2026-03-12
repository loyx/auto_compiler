# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_block_package._parse_block_src import _parse_block
from ._consume_token_package._consume_token_src import _consume_token

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_if_stmt(parser_state: ParserState) -> AST:
    """
    解析 if 语句。
    语法：IF '(' condition ')' block [ELSE block]
    输出：IF AST 节点，包含 condition、then_block、else_block。
    """
    tokens = parser_state["tokens"]
    filename = parser_state["filename"]
    pos = parser_state["pos"]
    
    # 1. 记录 IF token 的行号和列号
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input, expected IF statement")
    
    if_token = tokens[pos]
    start_line = if_token["line"]
    start_column = if_token["column"]
    
    # 2. 消费 IF token
    _consume_token(parser_state, "IF")
    
    # 3. 消费 LPAREN token
    _consume_token(parser_state, "LPAREN")
    
    # 4. 解析条件表达式
    condition = _parse_expression(parser_state)
    
    # 5. 消费 RPAREN token
    _consume_token(parser_state, "RPAREN")
    
    # 6. 解析 then 块
    then_block = _parse_block(parser_state)
    
    # 7. 检查是否有 ELSE token
    else_block = None
    current_pos = parser_state["pos"]
    if current_pos < len(tokens) and tokens[current_pos]["type"] == "ELSE":
        _consume_token(parser_state, "ELSE")
        else_block = _parse_block(parser_state)
    
    # 8. 构建 IF AST 节点
    if_node: AST = {
        "type": "IF",
        "condition": condition,
        "then_block": then_block,
        "else_block": else_block,
        "line": start_line,
        "column": start_column
    }
    
    return if_node

# === helper functions ===
# No additional helper functions needed; all logic delegated to sub-functions.

# === OOP compatibility layer ===
# Not required for this parser function node.
