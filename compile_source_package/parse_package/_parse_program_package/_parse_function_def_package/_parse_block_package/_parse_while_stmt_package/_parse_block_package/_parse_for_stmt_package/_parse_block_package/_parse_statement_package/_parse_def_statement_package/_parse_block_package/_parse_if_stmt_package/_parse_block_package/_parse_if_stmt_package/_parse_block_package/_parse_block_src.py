# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_stmt_package._parse_stmt_src import _parse_stmt

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
    
    支持两种风格：
    1. 花括号风格：LBRACE stmt* RBRACE
    2. 缩进风格：NEWLINE INDENT stmt+ DEDENT
    
    副作用：更新 parser_state['pos'] 到块结束后的位置。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input while parsing block")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    # 记录块起始位置
    block_line = current_token["line"]
    block_column = current_token["column"]
    
    children = []
    
    if token_type == "LBRACE":
        # 花括号风格：{ stmt* }
        pos += 1  # 消费 LBRACE
        
        while pos < len(tokens):
            if tokens[pos]["type"] == "RBRACE":
                pos += 1  # 消费 RBRACE
                break
            
            # 解析语句
            stmt_ast = _parse_stmt(parser_state)
            children.append(stmt_ast)
            pos = parser_state["pos"]
        
        if pos >= len(tokens) or tokens[pos - 1]["type"] != "RBRACE":
            raise SyntaxError(f"Missing RBRACE in block at line {block_line}")
    
    elif token_type == "NEWLINE":
        # 缩进风格：NEWLINE INDENT stmt+ DEDENT
        pos += 1  # 消费 NEWLINE
        
        if pos >= len(tokens) or tokens[pos]["type"] != "INDENT":
            raise SyntaxError(f"Expected INDENT after NEWLINE at line {block_line}")
        
        pos += 1  # 消费 INDENT
        
        while pos < len(tokens):
            if tokens[pos]["type"] == "DEDENT":
                pos += 1  # 消费 DEDENT
                break
            
            # 解析语句
            stmt_ast = _parse_stmt(parser_state)
            children.append(stmt_ast)
            pos = parser_state["pos"]
        
        if pos >= len(tokens) or tokens[pos - 1]["type"] != "DEDENT":
            raise SyntaxError(f"Missing DEDENT in block at line {block_line}")
    
    else:
        raise SyntaxError(
            f"Expected LBRACE or NEWLINE to start block, got {token_type} "
            f"at line {block_line}, column {block_column}"
        )
    
    # 更新 parser_state 位置
    parser_state["pos"] = pos
    
    # 构建 BLOCK AST 节点
    block_ast: AST = {
        "type": "BLOCK",
        "line": block_line,
        "column": block_column,
        "children": children
    }
    
    return block_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function