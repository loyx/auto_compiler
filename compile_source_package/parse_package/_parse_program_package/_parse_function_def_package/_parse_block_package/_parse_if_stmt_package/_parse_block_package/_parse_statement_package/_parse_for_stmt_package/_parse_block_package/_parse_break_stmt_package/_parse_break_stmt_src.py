# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions for this simple parser node

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
def _parse_break_stmt(parser_state: ParserState) -> AST:
    """
    解析 BREAK 语句。
    
    语法：break ;
    
    输入：parser_state（pos 指向 BREAK token）
    输出：BREAK AST 节点
    副作用：修改 parser_state["pos"] 指向语句结束后的下一个 token
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 获取 BREAK token
    break_token = tokens[pos]
    line = break_token["line"]
    column = break_token["column"]
    
    # 消费 BREAK token
    pos += 1
    
    # 检查并消费 SEMICOLON
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{line}:{column}: expected ';' after 'break'")
    
    semicolon_token = tokens[pos]
    if semicolon_token["type"] != "SEMICOLON":
        raise SyntaxError(f"{filename}:{line}:{column}: expected ';' after 'break', got '{semicolon_token['value']}'")
    
    # 消费 SEMICOLON token
    pos += 1
    
    # 更新 parser_state 位置
    parser_state["pos"] = pos
    
    # 构建 BREAK AST 节点
    ast_node: AST = {
        "type": "BREAK",
        "line": line,
        "column": column
    }
    
    return ast_node

# === helper functions ===
# No helper functions needed for this simple parser

# === OOP compatibility layer ===
# Not needed for parser function nodes
