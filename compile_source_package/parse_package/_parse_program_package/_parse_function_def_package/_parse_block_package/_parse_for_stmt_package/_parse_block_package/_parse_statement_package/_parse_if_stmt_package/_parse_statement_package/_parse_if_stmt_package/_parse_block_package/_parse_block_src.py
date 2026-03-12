# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_statement_package._parse_statement_src import _parse_statement

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,           # 如 "LBRACE", "RBRACE", "IDENT", "SEMICOLON" 等
#   "value": str,          # token 原始文本
#   "line": int,           # 行号
#   "column": int          # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,           # 节点类型，如 "BLOCK", "EXPR_STMT", "IF_STMT" 等
#   "children": list,      # 子节点 AST 列表
#   "value": Any,          # 节点值（可选）
#   "line": int,           # 起始行号
#   "column": int          # 起始列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,        # Token 列表
#   "pos": int,            # 当前解析位置索引
#   "filename": str,       # 源文件名
#   "error": str           # 错误信息（可选）
# }

# === main function ===
def _parse_block(parser_state: ParserState) -> AST:
    """解析代码块 { statement* }。
    
    输入：parser_state（pos 指向 LBRACE token）
    输出：BLOCK AST 节点，children 包含块内所有语句 AST
    副作用：更新 parser_state['pos'] 到 RBRACE 之后
    异常：语法错误时抛出 SyntaxError
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 验证当前 token 是 LBRACE
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected '{'")
    
    current_token = tokens[pos]
    if current_token["type"] != "LBRACE":
        raise SyntaxError(f"Expected '{{' but got {current_token['type']}")
    
    block_line = current_token["line"]
    block_column = current_token["column"]
    
    # 跳过 LBRACE
    parser_state["pos"] = pos + 1
    pos = parser_state["pos"]
    
    # 解析块内语句
    children = []
    while pos < len(tokens):
        current_token = tokens[pos]
        
        # 检查是否到达 RBRACE
        if current_token["type"] == "RBRACE":
            # 跳过 RBRACE
            parser_state["pos"] = pos + 1
            break
        
        # 解析一条语句
        stmt_ast = _parse_statement(parser_state)
        children.append(stmt_ast)
        pos = parser_state["pos"]
    else:
        # 循环正常结束但未遇到 RBRACE
        raise SyntaxError("Unexpected end of input, expected '}'")
    
    # 构建 BLOCK AST 节点
    block_ast: AST = {
        "type": "BLOCK",
        "children": children,
        "value": None,
        "line": block_line,
        "column": block_column
    }
    
    return block_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser internal functions
