# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_logical_not_package._parse_logical_not_src import _parse_logical_not

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (e.g., "AND", "IDENTIFIER", "NUMBER")
#   "value": str,            # token 值 (e.g., "and", "x", "42")
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值 (操作符名称或字面量值)
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
def _parse_logical_and(parser_state: ParserState) -> AST:
    """
    解析逻辑与表达式（AND 运算符）。
    实现左结合的 AND 运算解析。
    """
    # 先调用 _parse_logical_not 解析左侧表达式
    left_node = _parse_logical_not(parser_state)
    
    # 检查是否有错误
    if parser_state.get('error'):
        return left_node
    
    # 循环处理多个 AND 运算符（左结合）
    while True:
        current_pos = parser_state.get('pos', 0)
        tokens = parser_state.get('tokens', [])
        
        # 检查是否到达 token 末尾
        if current_pos >= len(tokens):
            break
        
        current_token = tokens[current_pos]
        
        # 检查当前 token 是否为 AND 运算符
        is_and = (current_token.get('type') == 'AND' or 
                  current_token.get('value') == 'and')
        
        if not is_and:
            break
        
        # 消费 AND token
        parser_state['pos'] = current_pos + 1
        and_token = current_token
        
        # 解析右侧表达式
        right_node = _parse_logical_not(parser_state)
        
        # 检查是否有错误
        if parser_state.get('error'):
            return left_node
        
        # 构建 BINARY_OP 节点
        left_node = {
            'type': 'BINARY_OP',
            'children': [left_node, right_node],
            'value': 'AND',
            'line': and_token.get('line', 0),
            'column': and_token.get('column', 0)
        }
    
    return left_node


# === helper functions ===
# No helper functions needed for this simple parsing logic

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function nodes
