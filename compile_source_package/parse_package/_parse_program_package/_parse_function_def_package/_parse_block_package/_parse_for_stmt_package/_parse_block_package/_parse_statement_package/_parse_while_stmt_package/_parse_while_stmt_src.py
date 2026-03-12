# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_statement_package._parse_statement_src import _parse_statement
from ._expect_token_package._expect_token_src import _expect_token

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
#   "type": str,             # 节点类型 (PROGRAM, FUNCTION_DEF, PARAM, VAR_DECL, IF_STMT, WHILE_STMT, FOR_STMT, RETURN_STMT, BREAK_STMT, CONTINUE_STMT, EXPR_STMT, BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, BLOCK)
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
def _parse_while_stmt(parser_state: ParserState) -> AST:
    """
    解析 while 语句。
    
    语法格式：while (expression) statement
    
    参数:
        parser_state: ParserState - 解析器状态字典，调用时 pos 指向 WHILE token
        
    返回:
        AST - WHILE_STMT 类型 AST 节点，包含条件表达式和循环体
        
    副作用:
        原地更新 parser_state["pos"] 到语句结束位置（RBRACE 之后）
        
    异常:
        遇到语法错误（缺少括号、语句等）时抛出 SyntaxError
    """
    # 1. 消耗 WHILE 关键字
    _expect_token(parser_state, "WHILE")
    
    # 2. 消耗左括号
    _expect_token(parser_state, "LPAREN")
    
    # 3. 解析条件表达式
    condition_ast = _parse_expression(parser_state)
    
    # 4. 消耗右括号
    _expect_token(parser_state, "RPAREN")
    
    # 5. 消耗左大括号（循环体开始）
    _expect_token(parser_state, "LBRACE")
    
    # 6. 解析循环体（单条语句或语句块）
    body_ast = _parse_statement(parser_state)
    
    # 7. 消耗右大括号（循环体结束）
    _expect_token(parser_state, "RBRACE")
    
    # 8. 构建 WHILE_STMT AST 节点
    return {
        "type": "WHILE_STMT",
        "children": [condition_ast, body_ast],
        "line": condition_ast.get("line", 0),
        "column": condition_ast.get("column", 0)
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
