# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_statement_package._parse_statement_src import _parse_statement

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
def _parse_block(parser_state: ParserState) -> AST:
    """
    解析代码块。
    
    block 语法：LBRACE statement* RBRACE
    输出 AST 结构：{"type": "BLOCK", "line": int, "column": int, "children": [statement ASTs]}
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查并消费 LBRACE
    if pos >= len(tokens):
        raise SyntaxError("Expected '{' at block start")
    
    current_token = tokens[pos]
    if current_token["type"] != "LBRACE":
        raise SyntaxError("Expected '{' at block start")
    
    block_line = current_token["line"]
    block_column = current_token["column"]
    pos += 1  # 消费 LBRACE
    
    # 解析语句序列
    children = []
    while pos < len(tokens):
        current_token = tokens[pos]
        
        # 检查是否遇到 RBRACE
        if current_token["type"] == "RBRACE":
            pos += 1  # 消费 RBRACE
            break
        
        # 解析当前语句
        parser_state["pos"] = pos
        statement_ast = _parse_statement(parser_state)
        children.append(statement_ast)
        pos = parser_state["pos"]
    else:
        # 循环正常结束但未遇到 RBRACE
        raise SyntaxError("Expected '}' at block end")
    
    # 更新 parser_state
    parser_state["pos"] = pos
    
    # 构建 BLOCK AST 节点
    return {
        "type": "BLOCK",
        "line": block_line,
        "column": block_column,
        "children": children
    }

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# Not needed for parser function nodes