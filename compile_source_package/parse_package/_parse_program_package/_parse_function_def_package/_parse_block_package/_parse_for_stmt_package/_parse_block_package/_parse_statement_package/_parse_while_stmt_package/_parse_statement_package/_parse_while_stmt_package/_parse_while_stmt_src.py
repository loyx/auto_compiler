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
def _parse_while_stmt(parser_state: ParserState) -> AST:
    """
    解析 while 语句。语法：while ( 条件 ) 语句块
    输入 parser_state（pos 指向 WHILE token），返回 WHILE_STMT AST 节点。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # Step 1: 当前 token 必须是 WHILE
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: 意外的文件结束，期望 'while'")
    
    current_token = tokens[pos]
    if current_token["type"] != "WHILE":
        raise SyntaxError(
            f"{filename}:{current_token['line']}:{current_token['column']}: "
            f"期望 'while'，得到 '{current_token['value']}'"
        )
    
    while_line = current_token["line"]
    while_column = current_token["column"]
    
    # Step 2: 消耗 WHILE token
    pos += 1
    
    # Step 3: 下一个 token 必须是 LPAREN
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: 意外的文件结束，期望 '('")
    
    current_token = tokens[pos]
    if current_token["type"] != "LPAREN":
        raise SyntaxError(
            f"{filename}:{current_token['line']}:{current_token['column']}: "
            f"期望 '('，得到 '{current_token['value']}'"
        )
    
    # Step 4: 消耗 LPAREN
    pos += 1
    
    # Step 5: 解析条件表达式
    parser_state["pos"] = pos
    condition_ast = _parse_expression(parser_state)
    pos = parser_state["pos"]
    
    # Step 6: 下一个 token 必须是 RPAREN
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: 意外的文件结束，期望 ')'")
    
    current_token = tokens[pos]
    if current_token["type"] != "RPAREN":
        raise SyntaxError(
            f"{filename}:{current_token['line']}:{current_token['column']}: "
            f"期望 ')'，得到 '{current_token['value']}'"
        )
    
    # Step 7: 消耗 RPAREN
    pos += 1
    
    # Step 8: 解析循环体语句块
    parser_state["pos"] = pos
    body_ast = _parse_block(parser_state)
    pos = parser_state["pos"]
    
    # Step 9: 返回 WHILE_STMT AST 节点
    return {
        "type": "WHILE_STMT",
        "children": [condition_ast, body_ast],
        "line": while_line,
        "column": while_column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
