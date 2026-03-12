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
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_if_stmt(parser_state: dict) -> dict:
    """
    解析 if 语句。
    
    语法格式：if (条件) 语句块 [else 语句块]
    输入：parser_state（当前位置指向 IF 关键字）
    输出：IF_STMT 类型 AST 节点
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input: expected IF keyword")
    
    if_token = tokens[pos]
    line = if_token.get("line", 0)
    column = if_token.get("column", 0)
    
    # 1. 消费 IF 关键字
    parser_state = _consume_token(parser_state, "IF")
    
    # 2. 消费左括号
    parser_state = _consume_token(parser_state, "LPAREN")
    
    # 3. 解析条件表达式
    condition_ast = _parse_expression(parser_state)
    
    # 4. 消费右括号
    parser_state = _consume_token(parser_state, "RPAREN")
    
    # 5. 解析 then 块
    then_block_ast = _parse_block(parser_state)
    
    # 6. 检查是否有 ELSE 关键字
    children = [condition_ast, then_block_ast]
    pos = parser_state["pos"]
    
    if pos < len(tokens) and tokens[pos]["type"] == "ELSE":
        parser_state = _consume_token(parser_state, "ELSE")
        else_block_ast = _parse_block(parser_state)
        children.append(else_block_ast)
    
    # 7. 返回 IF_STMT AST 节点
    return {
        "type": "IF_STMT",
        "children": children,
        "line": line,
        "column": column
    }

# === helper functions ===

# === OOP compatibility layer ===
