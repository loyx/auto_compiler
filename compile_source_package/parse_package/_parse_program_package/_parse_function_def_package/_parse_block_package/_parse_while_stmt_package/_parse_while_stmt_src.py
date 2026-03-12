# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_block_package._parse_block_src import _parse_block

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
def _parse_while_stmt(parser_state: dict) -> dict:
    """
    解析 while 语句。
    
    输入：parser_state（当前位置指向 WHILE token）
    输出：WHILE_STMT 类型 AST 节点，包含 condition 和 body
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查当前 token 是否为 WHILE
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected WHILE statement")
    
    while_token = tokens[pos]
    if while_token["type"] != "WHILE":
        raise SyntaxError(f"Expected WHILE token, got {while_token['type']} at line {while_token['line']}")
    
    # 记录 while 语句的起始位置
    start_line = while_token["line"]
    start_column = while_token["column"]
    
    # 消费 WHILE token
    parser_state["pos"] = pos + 1
    
    # 解析条件表达式
    condition_node = _parse_expression(parser_state)
    
    # 解析循环主体块
    body_node = _parse_block(parser_state)
    
    # 构建 WHILE_STMT AST 节点
    while_node = {
        "type": "WHILE_STMT",
        "children": [condition_node, body_node],
        "line": start_line,
        "column": start_column
    }
    
    return while_node

# === helper functions ===
# No helper functions needed for this simple orchestration

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function