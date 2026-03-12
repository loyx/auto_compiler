# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_statement_package._parse_statement_src import _parse_statement

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BLOCK, EXPR_STMT, IF_STMT, WHILE_STMT, FOR_STMT, RETURN_STMT, BREAK_STMT, CONTINUE_STMT, VAR_DECL, 等)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }

# === main function ===
def _parse_block(parser_state: ParserState) -> AST:
    """
    解析代码块。从起始 token（如 LBRACE）到结束 token（如 RBRACE），
    返回 BLOCK 类型 AST 节点，包含块内所有语句。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 获取起始 token 位置信息
    start_token = tokens[pos]
    start_line = start_token.get("line", 0)
    start_column = start_token.get("column", 0)
    
    # 消耗块起始 token（如 LBRACE）
    pos += 1
    
    # 收集块内所有语句
    statements = []
    while pos < len(tokens):
        current_token = tokens[pos]
        
        # 检查是否遇到块结束 token
        if current_token.get("type") == "RBRACE":
            # 消耗块结束 token
            pos += 1
            break
        
        # 解析当前语句
        stmt_ast = _parse_statement(parser_state)
        statements.append(stmt_ast)
        pos = parser_state["pos"]
    
    # 更新 parser_state 位置
    parser_state["pos"] = pos
    
    # 构建 BLOCK AST 节点
    block_ast = {
        "type": "BLOCK",
        "children": statements,
        "value": None,
        "line": start_line,
        "column": start_column
    }
    
    return block_ast

# === helper functions ===
def _check_block_end(tokens: list, pos: int) -> bool:
    """检查当前位置是否为块结束 token。"""
    if pos >= len(tokens):
        return True
    return tokens[pos].get("type") == "RBRACE"

# === OOP compatibility layer ===
