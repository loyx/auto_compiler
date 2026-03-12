# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_if_stmt(parser_state: ParserState) -> AST:
    """
    解析 IF 语句。
    
    语法：'(' expression ')' block ('else' block)?
    
    输入：parser_state，其中 pos 指向 IF token
    输出：IF 类型 AST 节点，包含 condition、then_block、else_block
    """
    tokens = parser_state["tokens"]
    filename = parser_state["filename"]
    
    # 检查是否已到达文件末尾
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: 期望 IF 语句，但已到达文件末尾")
    
    # 记录 IF token 的位置信息
    current_token = tokens[parser_state["pos"]]
    line = current_token["line"]
    column = current_token["column"]
    
    # 消费 IF token
    _consume_token(parser_state, "IF")
    
    # 解析条件表达式
    condition = _parse_expression(parser_state)
    
    # 解析 then_block
    then_block = _parse_block(parser_state)
    
    # 检查是否有 else 分支
    else_block = None
    if parser_state["pos"] < len(tokens):
        next_token = tokens[parser_state["pos"]]
        if next_token["type"] == "ELSE":
            parser_state["pos"] += 1  # 消费 ELSE token
            else_block = _parse_block(parser_state)
    
    return {
        "type": "IF",
        "condition": condition,
        "then_block": then_block,
        "else_block": else_block,
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function nodes
