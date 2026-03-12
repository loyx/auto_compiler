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
    """解析语句块。语法：{ 语句列表 }"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 1. 当前 token 必须是 LBRACE
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:???:???: 期望 '{{' 但到达文件末尾")
    
    current_token = tokens[pos]
    if current_token.get("type") != "LBRACE":
        raise SyntaxError(
            f"{filename}:{current_token.get('line', '?')}:{current_token.get('column', '?')}: "
            f"期望 '{{' 但得到 '{current_token.get('value', '')}'"
        )
    
    # 记录块的起始位置
    start_line = current_token.get("line", 0)
    start_column = current_token.get("column", 0)
    
    # 2. 消耗 LBRACE token
    parser_state["pos"] = pos + 1
    
    # 3. 循环解析语句
    children = []
    while True:
        pos = parser_state["pos"]
        
        # 检查是否到达 RBRACE
        if pos >= len(tokens):
            raise SyntaxError(f"{filename}:???:???: 期望 '}}' 但到达文件末尾")
        
        current_token = tokens[pos]
        
        if current_token.get("type") == "RBRACE":
            # 4. 消耗 RBRACE
            parser_state["pos"] = pos + 1
            break
        
        # 解析一条语句
        statement_ast = _parse_statement(parser_state)
        children.append(statement_ast)
    
    # 5. 返回 BLOCK AST 节点
    return {
        "type": "BLOCK",
        "children": children,
        "line": start_line,
        "column": start_column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
