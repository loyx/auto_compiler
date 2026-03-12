# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_statement_package._parse_statement_src import _parse_statement

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,           # token type (e.g., "LBRACE", "RBRACE", "IDENT")
#   "value": str,          # token value (e.g., "{", "}", "x")
#   "line": int,           # source line number
#   "column": int          # source column number
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,           # node type (e.g., "BLOCK", "STATEMENT")
#   "children": list,      # list of child AST nodes
#   "value": str,          # node value (e.g., "{")
#   "line": int,           # source line number
#   "column": int          # source column number
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,        # list of Token
#   "pos": int,            # current position in tokens
#   "filename": str,       # source filename
#   "error": str           # error message (if any)
# }

# === main function ===
def _parse_block(parser_state: ParserState) -> AST:
    """
    解析代码块（由 {} 包裹的语句序列）。
    输入 parser_state（pos 指向 LBRACE token），返回 BLOCK AST 节点。
    副作用：更新 pos 到 RBRACE 之后。
    异常：语法错误抛出 SyntaxError（如缺少 RBRACE）。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. 消耗 LBRACE token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected '{'")
    
    lbrace_token = tokens[pos]
    if lbrace_token["type"] != "LBRACE":
        raise SyntaxError(f"Expected '{{', got {lbrace_token['type']}")
    
    block_line = lbrace_token["line"]
    block_column = lbrace_token["column"]
    pos += 1
    
    # 2. 循环解析语句，直到遇到 RBRACE token
    children = []
    while pos < len(tokens):
        current_token = tokens[pos]
        
        # 检查是否遇到 RBRACE
        if current_token["type"] == "RBRACE":
            break
        
        # 解析语句
        statement_ast = _parse_statement(parser_state)
        children.append(statement_ast)
        pos = parser_state["pos"]
    
    # 3. 消耗 RBRACE token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected '}'")
    
    rbrace_token = tokens[pos]
    if rbrace_token["type"] != "RBRACE":
        raise SyntaxError(f"Expected '}}', got {rbrace_token['type']}")
    
    pos += 1
    parser_state["pos"] = pos
    
    # 4. 构建 BLOCK AST 节点
    block_ast: AST = {
        "type": "BLOCK",
        "children": children,
        "value": "{",
        "line": block_line,
        "column": block_column
    }
    
    return block_ast

# === helper functions ===
# No helper functions needed; logic is straightforward

# === OOP compatibility layer ===
# Not needed for parser function nodes
