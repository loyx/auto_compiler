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
def _parse_if_stmt(parser_state: ParserState) -> AST:
    """解析 if 语句。输入：parser_state（pos 指向 IF token）。输出：IF AST 节点。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. 消费 IF token
    if_token = _expect_token(tokens, pos, "IF")
    if_line = if_token["line"]
    if_column = if_token["column"]
    pos += 1
    
    # 2. 解析条件表达式
    condition_ast = _parse_expr(parser_state)
    pos = parser_state["pos"]
    
    # 3. 消费 COLON token
    colon_token = _expect_token(tokens, pos, "COLON")
    pos += 1
    
    # 4. 解析 if 块
    if_block_ast = _parse_block(parser_state)
    pos = parser_state["pos"]
    
    # 5. 构建 children 列表
    children = [condition_ast, if_block_ast]
    
    # 6. 循环处理 ELIF 分支
    while pos < len(tokens) and tokens[pos]["type"] == "ELIF":
        pos += 1  # 消费 ELIF
        
        # 解析 ELIF 条件
        parser_state["pos"] = pos
        elif_condition_ast = _parse_expr(parser_state)
        pos = parser_state["pos"]
        
        # 消费 COLON
        _expect_token(tokens, pos, "COLON")
        pos += 1
        
        # 解析 ELIF 块
        parser_state["pos"] = pos
        elif_block_ast = _parse_block(parser_state)
        pos = parser_state["pos"]
        
        # 构建 ELIF 分支节点
        elif_branch = {
            "type": "ELIF",
            "line": tokens[pos - 1]["line"],
            "column": tokens[pos - 1]["column"],
            "children": [elif_condition_ast, elif_block_ast]
        }
        children.append(elif_branch)
    
    # 7. 处理 ELSE 分支
    if pos < len(tokens) and tokens[pos]["type"] == "ELSE":
        pos += 1  # 消费 ELSE
        
        # 消费 COLON
        _expect_token(tokens, pos, "COLON")
        pos += 1
        
        # 解析 ELSE 块
        parser_state["pos"] = pos
        else_block_ast = _parse_block(parser_state)
        pos = parser_state["pos"]
        
        children.append(else_block_ast)
    
    # 8. 消费 SEMICOLON token
    _expect_token(tokens, pos, "SEMICOLON")
    pos += 1
    
    # 更新 parser_state
    parser_state["pos"] = pos
    
    # 构建 IF AST 节点
    return {
        "type": "IF",
        "line": if_line,
        "column": if_column,
        "children": children
    }

# === helper functions ===
def _expect_token(tokens: list, pos: int, token_type: str) -> Token:
    """期望当前 token 为指定类型，否则抛出 SyntaxError。"""
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input, expected {token_type}")
    token = tokens[pos]
    if token["type"] != token_type:
        raise SyntaxError(f"Expected {token_type}, got {token['type']} at line {token['line']}, column {token['column']}")
    return token

# === OOP compatibility layer ===
