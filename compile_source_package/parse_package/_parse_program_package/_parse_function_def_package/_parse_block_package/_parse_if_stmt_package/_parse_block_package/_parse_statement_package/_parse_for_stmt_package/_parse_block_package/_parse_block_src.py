# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_for_stmt_package._parse_for_stmt_src import _parse_for_stmt
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
from ._parse_break_stmt_package._parse_break_stmt_src import _parse_break_stmt
from ._parse_continue_stmt_package._parse_continue_stmt_src import _parse_continue_stmt
from ._parse_var_decl_stmt_package._parse_var_decl_stmt_src import _parse_var_decl_stmt
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
    """
    解析语句块 { ... }。
    输入：parser_state（pos 指向 LBRACE token）
    输出：BLOCK AST 节点（type="BLOCK", children 包含语句 AST 列表）
    副作用：修改 parser_state["pos"] 指向 RBRACE 后的下一个 token
    """
    tokens = parser_state["tokens"]
    filename = parser_state["filename"]
    
    # 消费 LBRACE
    lbrace_token = _current_token(parser_state)
    if lbrace_token["type"] != "LBRACE":
        raise SyntaxError(f"{filename}:{lbrace_token['line']}:{lbrace_token['column']}: 期望 LBRACE")
    
    block_line = lbrace_token["line"]
    block_column = lbrace_token["column"]
    _advance(parser_state)
    
    children = []
    
    # 循环解析块内语句，直到遇到 RBRACE
    while True:
        token = _current_token(parser_state)
        
        # 检查是否到达文件末尾
        if token is None:
            raise SyntaxError(f"{filename}:{block_line}:{block_column}: 未找到 RBRACE，块未闭合")
        
        # 遇到 RBRACE，结束块解析
        if token["type"] == "RBRACE":
            _advance(parser_state)
            break
        
        # 根据 token type 分发到相应的语句解析函数
        stmt_ast = _parse_statement(parser_state, token, filename)
        children.append(stmt_ast)
    
    return {
        "type": "BLOCK",
        "children": children,
        "line": block_line,
        "column": block_column
    }

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """获取当前位置的 token，如果越界则返回 None。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        return None
    return tokens[pos]

def _advance(parser_state: ParserState) -> None:
    """将 parser_state["pos"] 向前移动一位。"""
    parser_state["pos"] += 1

def _parse_statement(parser_state: ParserState, token: Token, filename: str) -> AST:
    """
    根据 token type 分发到相应的语句解析函数。
    """
    token_type = token["type"]
    
    # 语句类型到解析函数的映射
    dispatch_map = {
        "IF": _parse_if_stmt,
        "FOR": _parse_for_stmt,
        "WHILE": _parse_while_stmt,
        "RETURN": _parse_return_stmt,
        "BREAK": _parse_break_stmt,
        "CONTINUE": _parse_continue_stmt,
        "VAR": _parse_var_decl_stmt,
        "LBRACE": _parse_block,  # 嵌套块，递归调用自身
    }
    
    if token_type in dispatch_map:
        return dispatch_map[token_type](parser_state)
    
    # 其他情况视为表达式语句
    # 但需要排除明显非法的 token
    if token_type == "RBRACE":
        # 不应该在这里遇到 RBRACE，因为外层循环会处理
        raise SyntaxError(f"{filename}:{token['line']}:{token['column']}: 意外的 RBRACE")
    
    return _parse_expression_stmt(parser_state)

# === OOP compatibility layer ===
# 本模块为解析器内部函数节点，不需要 OOP wrapper
