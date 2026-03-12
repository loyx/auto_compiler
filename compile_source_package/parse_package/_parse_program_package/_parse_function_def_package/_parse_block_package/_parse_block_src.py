# === std / third-party imports ===
from typing import Any, Dict

# === ADT defines ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]

# === main function ===
def _parse_block(parser_state: ParserState) -> AST:
    """解析语句块（花括号包裹的零个或多个语句）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 消费左花括号 '{'
    if pos >= len(tokens) or tokens[pos]["type"] != "LBRACE":
        line = tokens[pos]["line"] if pos < len(tokens) else "EOF"
        column = tokens[pos]["column"] if pos < len(tokens) else "0"
        raise SyntaxError(f"Syntax error at {filename}:{line}:{column} - Expected '{{'")
    
    start_line = tokens[pos]["line"]
    start_column = tokens[pos]["column"]
    pos += 1
    
    children = []
    
    # 循环解析语句，直到遇到右花括号 '}'
    while pos < len(tokens) and tokens[pos]["type"] != "RBRACE":
        stmt_node, pos = _parse_statement(tokens, pos, filename)
        children.append(stmt_node)
    
    # 消费右花括号 '}'
    if pos >= len(tokens) or tokens[pos]["type"] != "RBRACE":
        line = tokens[pos]["line"] if pos < len(tokens) else "EOF"
        column = tokens[pos]["column"] if pos < len(tokens) else "0"
        raise SyntaxError(f"Syntax error at {filename}:{line}:{column} - Expected '}}'")
    pos += 1
    
    parser_state["pos"] = pos
    
    return {
        "type": "BLOCK",
        "children": children,
        "line": start_line,
        "column": start_column
    }

# === helper functions ===
def _parse_statement(tokens: list, pos: int, filename: str) -> tuple:
    """根据 token 类型分发到相应的语句解析函数。"""
    if pos >= len(tokens):
        raise SyntaxError(f"Syntax error at {filename}:EOF:0 - Unexpected end of file")
    
    token = tokens[pos]
    token_type = token["type"]
    
    # 创建临时 parser_state 供子函数使用
    temp_state = {"tokens": tokens, "pos": pos, "filename": filename}
    
    # 延迟导入子函数（仅在需要时）
    if token_type == "IF":
        from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
        node = _parse_if_stmt(temp_state)
    elif token_type == "WHILE":
        from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
        node = _parse_while_stmt(temp_state)
    elif token_type == "FOR":
        from ._parse_for_stmt_package._parse_for_stmt_src import _parse_for_stmt
        node = _parse_for_stmt(temp_state)
    elif token_type == "RETURN":
        from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
        node = _parse_return_stmt(temp_state)
    elif token_type == "BREAK":
        from ._parse_break_stmt_package._parse_break_stmt_src import _parse_break_stmt
        node = _parse_break_stmt(temp_state)
    elif token_type == "CONTINUE":
        from ._parse_continue_stmt_package._parse_continue_stmt_src import _parse_continue_stmt
        node = _parse_continue_stmt(temp_state)
    elif token_type in ("INT", "FLOAT", "BOOL", "STRING"):
        # 类型标识符后跟 IDENTIFIER 是变量声明
        if pos + 1 < len(tokens) and tokens[pos + 1]["type"] == "IDENTIFIER":
            from ._parse_var_decl_package._parse_var_decl_src import _parse_var_decl
            node = _parse_var_decl(temp_state)
        else:
            from ._parse_expr_stmt_package._parse_expr_stmt_src import _parse_expr_stmt
            node = _parse_expr_stmt(temp_state)
    elif token_type == "IDENTIFIER":
        # IDENTIFIER 可能是表达式语句或变量声明（如果有类型前缀，但这里已经处理了）
        from ._parse_expr_stmt_package._parse_expr_stmt_src import _parse_expr_stmt
        node = _parse_expr_stmt(temp_state)
    else:
        # 其他情况作为表达式语句
        from ._parse_expr_stmt_package._parse_expr_stmt_src import _parse_expr_stmt
        node = _parse_expr_stmt(temp_state)
    
    return node, temp_state["pos"]

# === OOP compatibility layer ===
