# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Note: Using lazy import pattern to allow mocking in tests
# Imports are done inside the function to enable patching

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
    """解析语句块，返回 BLOCK 类型 AST 节点。"""
    # Lazy imports to allow mocking in tests
    from ._parse_statement_package._parse_statement_src import _parse_statement
    from ._expect_token_package._expect_token_src import _expect_token
    
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查当前位置是否有效
    if pos >= len(tokens):
        raise SyntaxError(f"Expected '{{' at end of file")
    
    current_token = tokens[pos]
    block_line = current_token["line"]
    block_column = current_token["column"]
    
    # 消费起始 LBRACE
    _expect_token(parser_state, "LBRACE", "{")
    
    # 收集块内语句
    children = []
    
    # 循环解析语句，直到遇到 RBRACE
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        # 检查是否遇到块结束标记
        if current_token["type"] == "RBRACE":
            break
        
        # 解析当前语句
        stmt_ast = _parse_statement(parser_state)
        children.append(stmt_ast)
    
    # 消费结束 RBRACE
    _expect_token(parser_state, "RBRACE", "}")
    
    # 构建 BLOCK 节点
    return {
        "type": "BLOCK",
        "children": children,
        "line": block_line,
        "column": block_column
    }

# === helper functions ===

# === OOP compatibility layer ===
