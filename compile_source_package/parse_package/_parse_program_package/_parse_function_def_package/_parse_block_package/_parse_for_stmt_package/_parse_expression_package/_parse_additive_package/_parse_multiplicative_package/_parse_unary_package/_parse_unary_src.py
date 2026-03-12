# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary

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
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, etc.)
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
def _parse_unary(parser_state: ParserState) -> AST:
    """
    解析一元表达式（前缀运算符如 +, -, not 等）。
    支持链式一元运算符（如 ---x, not not x）。
    """
    tokens = parser_state['tokens']
    pos = parser_state['pos']
    
    # 边界检查：如果已超出 token 列表
    if pos >= len(tokens):
        parser_state['error'] = "Unexpected end of input"
        return {'type': 'ERROR', 'value': '', 'children': [], 'line': 0, 'column': 0}
    
    token = tokens[pos]
    
    # 检查是否为一元运算符
    if token['type'] in ('PLUS', 'MINUS', 'NOT'):
        op = token['value']
        parser_state['pos'] += 1
        
        # 递归解析操作数（支持链式一元运算符）
        operand = _parse_unary(parser_state)
        
        return {
            'type': 'UNARY_OP',
            'value': op,
            'children': [operand],
            'line': token['line'],
            'column': token['column']
        }
    else:
        # 不是运算符，解析基础表达式
        return _parse_primary(parser_state)

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function nodes
