# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
from ._parse_assignment_package._parse_assignment_src import _parse_assignment
from ._parse_expr_stmt_package._parse_expr_stmt_src import _parse_expr_stmt

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
    """解析语句块（COLON 之后到 SEMICOLON 之前的所有语句）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 记录块起始位置（COLON 的位置，由调用者提供）
    if pos < len(tokens):
        block_line = tokens[pos]["line"]
        block_column = tokens[pos]["column"]
    else:
        block_line = 0
        block_column = 0
    
    children = []
    
    # 循环解析语句，直到遇到 SEMICOLON 或 EOF
    while pos < len(tokens):
        current_token = tokens[pos]
        
        # 遇到 SEMICOLON，块结束
        if current_token["type"] == "SEMICOLON":
            pos += 1
            parser_state["pos"] = pos
            return {
                "type": "BODY",
                "line": block_line,
                "column": block_column,
                "children": children
            }
        
        # 根据 token 类型分发到对应的解析函数
        if current_token["type"] == "IF":
            stmt_ast = _parse_if_stmt(parser_state)
            children.append(stmt_ast)
        elif current_token["type"] == "WHILE":
            stmt_ast = _parse_while_stmt(parser_state)
            children.append(stmt_ast)
        elif current_token["type"] == "IDENT":
            stmt_ast = _parse_assignment(parser_state)
            children.append(stmt_ast)
        else:
            # 其他情况按表达式语句处理
            stmt_ast = _parse_expr_stmt(parser_state)
            children.append(stmt_ast)
        
        pos = parser_state["pos"]
    
    # 循环结束仍未遇到 SEMICOLON，抛出语法错误
    raise SyntaxError(f"Expected SEMICOLON at line {block_line}")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
