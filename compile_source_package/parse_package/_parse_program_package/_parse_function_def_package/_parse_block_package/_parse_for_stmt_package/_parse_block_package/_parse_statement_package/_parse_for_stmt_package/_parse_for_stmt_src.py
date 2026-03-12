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
#   "type": str,             # 节点类型
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
def _parse_for_stmt(parser_state: ParserState) -> AST:
    """解析 for 语句。语法：for identifier in expression statement"""
    tokens = parser_state["tokens"]
    
    # 记录 FOR token 位置
    for_token = _expect(parser_state, "FOR")
    start_line = for_token["line"]
    start_column = for_token["column"]
    
    # 解析迭代变量标识符
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError("Unexpected end of input after 'for', expected identifier")
    identifier_token = tokens[parser_state["pos"]]
    if identifier_token["type"] != "IDENTIFIER":
        raise SyntaxError(
            f"Expected identifier after 'for', got {identifier_token['type']} "
            f"at line {identifier_token['line']}"
        )
    parser_state["pos"] += 1
    
    iter_var_node = {
        "type": "IDENTIFIER",
        "value": identifier_token["value"],
        "line": identifier_token["line"],
        "column": identifier_token["column"]
    }
    
    # 消耗 IN token
    _expect(parser_state, "IN")
    
    # 解析范围表达式
    range_expr_node = _parse_expression(parser_state)
    
    # 解析循环体（代码块或语句）
    body_node = _parse_block(parser_state)
    
    # 组装 FOR_STMT AST 节点
    return {
        "type": "FOR_STMT",
        "children": [iter_var_node, range_expr_node, body_node],
        "line": start_line,
        "column": start_column
    }

# === helper functions ===
def _expect(parser_state: ParserState, expected_type: str) -> Token:
    """期望并消耗指定类型的 token。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input, expected {expected_type}")
    
    token = tokens[pos]
    if token["type"] != expected_type:
        raise SyntaxError(
            f"Expected token type {expected_type}, got {token['type']} "
            f"at line {token['line']}"
        )
    
    parser_state["pos"] += 1
    return token

# === OOP compatibility layer ===
# No OOP wrapper needed for parser helper function
