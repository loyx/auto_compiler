# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._expect_token_package._expect_token_src import _expect_token
from ._parse_expression_package._parse_expression_src import _parse_expression
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
def _parse_if_stmt(parser_state: dict) -> dict:
    """
    解析 if 语句。语法格式：if (expression) statement [else statement]
    
    输入：parser_state（pos 指向 IF token）
    输出：IF_STMT 类型 AST 节点
    副作用：原地更新 parser_state["pos"] 到语句结束位置
    """
    tokens = parser_state["tokens"]
    start_pos = parser_state["pos"]
    
    # 1. 消耗 IF token
    if_token = tokens[start_pos]
    parser_state["pos"] += 1
    
    # 2. 消耗左括号
    _expect_token(parser_state, "LPAREN")
    
    # 3. 解析条件表达式
    condition = _parse_expression(parser_state)
    
    # 4. 消耗右括号
    _expect_token(parser_state, "RPAREN")
    
    # 5. 解析 then 分支语句
    then_stmt = _parse_statement(parser_state)
    
    # 6. 检查是否有 ELSE token
    else_stmt = None
    current_pos = parser_state["pos"]
    if current_pos < len(tokens) and tokens[current_pos]["type"] == "ELSE":
        parser_state["pos"] += 1
        else_stmt = _parse_statement(parser_state)
    
    # 7. 构建 IF_STMT AST 节点
    if_node = {
        "type": "IF_STMT",
        "children": [condition, then_stmt],
        "value": None,
        "line": if_token["line"],
        "column": if_token["column"]
    }
    
    if else_stmt is not None:
        if_node["children"].append(else_stmt)
    
    return if_node

# === helper functions ===
# No helper functions needed - logic is delegated to sub-functions

# === OOP compatibility layer ===
# Not needed for parser sub-function