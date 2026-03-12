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
def _parse_for_stmt(parser_state: ParserState) -> AST:
    """解析 for 语句，返回 FOR_STMT 类型 AST 节点。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 步骤 1: 消费 FOR token
    if pos >= len(tokens) or tokens[pos]["type"] != "FOR":
        raise SyntaxError(f"Expected FOR token at position {pos}")
    for_token = tokens[pos]
    pos += 1
    
    # 步骤 2: 解析变量名 (IDENTIFIER)
    if pos >= len(tokens) or tokens[pos]["type"] != "IDENTIFIER":
        raise SyntaxError(f"Expected IDENTIFIER after FOR at line {for_token['line']}")
    var_token = tokens[pos]
    variable_node = {
        "type": "IDENTIFIER",
        "value": var_token["value"],
        "line": var_token["line"],
        "column": var_token["column"],
        "children": []
    }
    pos += 1
    
    # 步骤 3: 消费 IN token
    if pos >= len(tokens) or tokens[pos]["type"] != "IN":
        raise SyntaxError(f"Expected IN token at line {var_token['line']}")
    in_token = tokens[pos]
    pos += 1
    
    # 步骤 4: 解析可迭代对象表达式
    parser_state["pos"] = pos
    iterable_node = _parse_expression(parser_state)
    pos = parser_state["pos"]
    
    # 步骤 5: 解析循环主体块 (期望冒号后跟块)
    if pos >= len(tokens) or tokens[pos]["type"] != "COLON":
        raise SyntaxError(f"Expected COLON after iterable expression at line {iterable_node.get('line', 'unknown')}")
    pos += 1
    
    parser_state["pos"] = pos
    body_node = _parse_block(parser_state)
    pos = parser_state["pos"]
    
    # 步骤 6: 返回 FOR_STMT 节点
    for_stmt_node = {
        "type": "FOR_STMT",
        "children": [variable_node, iterable_node, body_node],
        "line": for_token["line"],
        "column": for_token["column"]
    }
    
    parser_state["pos"] = pos
    return for_stmt_node

# === helper functions ===
def _consume_token(parser_state: ParserState, expected_type: str) -> Token:
    """消费指定类型的 token，不匹配则抛出 SyntaxError。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input, expected {expected_type}")
    
    token = tokens[pos]
    if token["type"] != expected_type:
        raise SyntaxError(f"Expected {expected_type} but got {token['type']} at line {token['line']}")
    
    parser_state["pos"] = pos + 1
    return token

# === OOP compatibility layer ===