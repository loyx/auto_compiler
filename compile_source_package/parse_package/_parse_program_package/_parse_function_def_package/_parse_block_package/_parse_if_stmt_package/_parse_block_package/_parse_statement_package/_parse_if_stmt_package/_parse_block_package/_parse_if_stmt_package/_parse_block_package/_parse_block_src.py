# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
from ._parse_assignment_package._parse_assignment_src import _parse_assignment
from ._parse_expression_stmt_package._parse_expression_stmt_src import _parse_expression_stmt
from ._parse_declaration_package._parse_declaration_src import _parse_declaration
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
from ._parse_for_stmt_package._parse_for_stmt_src import _parse_for_stmt

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_block(parser_state: ParserState) -> AST:
    """
    解析语句块。块的语法：'{' statement* '}'
    输入：parser_state（pos 指向 LBRACE token）
    输出：BLOCK AST 节点
    副作用：修改 parser_state["pos"] 到块结束位置
    """
    tokens = parser_state["tokens"]
    filename = parser_state["filename"]
    
    # 检查是否有 token 可读
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: 期望语句块起始 '{{'，但已到达文件末尾")
    
    current_token = tokens[parser_state["pos"]]
    line = current_token["line"]
    column = current_token["column"]
    
    # 1. 消费 LBRACE token
    _consume_token(parser_state, "LBRACE")
    
    # 2. 循环解析语句，直到遇到 RBRACE
    statements = []
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        # 检查是否遇到块结束
        if current_token["type"] == "RBRACE":
            break
        
        # 根据 lookahead token 分发到对应解析函数
        stmt = _parse_statement(parser_state, current_token)
        statements.append(stmt)
        
        # 消费可选的分号
        if parser_state["pos"] < len(tokens):
            next_token = tokens[parser_state["pos"]]
            if next_token["type"] == "SEMICOLON":
                parser_state["pos"] += 1
    
    # 3. 消费 RBRACE token
    _consume_token(parser_state, "RBRACE")
    
    # 4. 构建并返回 BLOCK AST 节点
    return {
        "type": "BLOCK",
        "statements": statements,
        "line": line,
        "column": column
    }

# === helper functions ===
def _parse_statement(parser_state: ParserState, token: Token) -> AST:
    """
    根据 lookahead token 分发到对应的语句解析函数。
    """
    token_type = token["type"]
    
    if token_type == "IF":
        return _parse_if_stmt(parser_state)
    elif token_type == "RETURN":
        return _parse_return_stmt(parser_state)
    elif token_type == "LET" or token_type == "CONST":
        return _parse_declaration(parser_state)
    elif token_type == "WHILE":
        return _parse_while_stmt(parser_state)
    elif token_type == "FOR":
        return _parse_for_stmt(parser_state)
    elif token_type == "IDENT":
        # 需要区分赋值语句和表达式语句
        return _parse_assignment_or_expression(parser_state)
    else:
        filename = parser_state["filename"]
        raise SyntaxError(f"{filename}:{token['line']}:{token['column']}: 未知的语句类型 '{token_type}'")

def _parse_assignment_or_expression(parser_state: ParserState) -> AST:
    """
    区分赋值语句和表达式语句。
    赋值语句：IDENT '=' expression
    表达式语句：expression
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 查看下一个 token 是否为赋值运算符
    if pos + 1 < len(tokens):
        next_token = tokens[pos + 1]
        if next_token["type"] == "ASSIGN":
            return _parse_assignment(parser_state)
    
    # 否则作为表达式语句处理
    return _parse_expression_stmt(parser_state)

# === OOP compatibility layer ===
# 本模块为纯函数解析器节点，不需要 OOP wrapper
