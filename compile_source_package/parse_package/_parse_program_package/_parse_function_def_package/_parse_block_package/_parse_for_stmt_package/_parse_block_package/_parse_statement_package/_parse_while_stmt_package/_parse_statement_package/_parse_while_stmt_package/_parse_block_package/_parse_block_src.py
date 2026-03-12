# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_for_stmt_package._parse_for_stmt_src import _parse_for_stmt
from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
from ._parse_assignment_stmt_package._parse_assignment_stmt_src import _parse_assignment_stmt
from ._parse_expression_stmt_package._parse_expression_stmt_src import _parse_expression_stmt

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
    """解析语句块。语法：{ 语句; 语句; ... }"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # 验证 LBRACE
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: 意外的文件结束，期望 '{{'")
    
    token = tokens[pos]
    if token["type"] != "LBRACE":
        raise SyntaxError(
            f"{filename}:{token['line']}:{token['column']}: "
            f"期望 '{{'，得到 '{token['value']}'"
        )
    
    block_line = token["line"]
    block_column = token["column"]
    pos += 1  # 消耗 LBRACE
    
    children = []
    
    # 解析语句直到 RBRACE
    while pos < len(tokens):
        current_token = tokens[pos]
        
        # 检查是否到达块结束
        if current_token["type"] == "RBRACE":
            pos += 1  # 消耗 RBRACE
            parser_state["pos"] = pos
            return {
                "type": "BLOCK",
                "children": children,
                "line": block_line,
                "column": block_column
            }
        
        # 根据首 token 类型分发到对应解析函数
        stmt_ast = _dispatch_statement(parser_state, current_token)
        children.append(stmt_ast)
        
        # 验证并消耗分号
        pos = parser_state["pos"]
        if pos >= len(tokens):
            raise SyntaxError(f"{filename}:0:0: 意外的文件结束，期望 ';'")
        
        semicolon_token = tokens[pos]
        if semicolon_token["type"] != "SEMICOLON":
            raise SyntaxError(
                f"{filename}:{semicolon_token['line']}:{semicolon_token['column']}: "
                f"期望 ';'，得到 '{semicolon_token['value']}'"
            )
        pos += 1
        parser_state["pos"] = pos
    
    # 到达 EOF 但未遇到 RBRACE
    raise SyntaxError(f"{filename}:0:0: 意外的文件结束，期望 '}}'")


# === helper functions ===
def _dispatch_statement(parser_state: ParserState, token: Token) -> AST:
    """根据 token 类型分发到对应的语句解析函数。"""
    token_type = token["type"]
    
    if token_type == "WHILE":
        return _parse_while_stmt(parser_state)
    elif token_type == "IF":
        return _parse_if_stmt(parser_state)
    elif token_type == "FOR":
        return _parse_for_stmt(parser_state)
    elif token_type == "RETURN":
        return _parse_return_stmt(parser_state)
    elif token_type == "IDENT":
        return _parse_assignment_stmt(parser_state)
    else:
        # 表达式语句
        return _parse_expression_stmt(parser_state)

# === OOP compatibility layer ===
