# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .._parse_unary_package._parse_unary_src import _parse_unary

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
def _parse_primary(parser_state: dict) -> dict:
    """解析基础表达式（标识符、字面量、括号表达式）。"""
    tokens = parser_state['tokens']
    pos = parser_state['pos']
    
    # 边界检查
    if pos >= len(tokens):
        parser_state['error'] = "Unexpected end of input"
        return {"type": "ERROR", "value": "", "children": [], "line": 0, "column": 0}
    
    token = tokens[pos]
    token_type = token['type']
    
    # 标识符
    if token_type == "IDENTIFIER":
        parser_state['pos'] += 1
        return {
            "type": "IDENTIFIER",
            "value": token['value'],
            "children": [],
            "line": token['line'],
            "column": token['column']
        }
    
    # 字面量
    if token_type in ("NUMBER", "STRING"):
        parser_state['pos'] += 1
        return {
            "type": "LITERAL",
            "value": token['value'],
            "children": [],
            "line": token['line'],
            "column": token['column']
        }
    
    # 括号表达式
    if token_type == "LPAREN":
        parser_state['pos'] += 1  # 消耗 LPAREN
        inner_expr = _parse_unary(parser_state)  # 解析括号内内容
        
        # 检查并消耗 RPAREN
        if parser_state['error']:
            return inner_expr
        
        current_pos = parser_state['pos']
        if current_pos < len(tokens) and tokens[current_pos]['type'] == "RPAREN":
            parser_state['pos'] += 1  # 消耗 RPAREN
            return inner_expr  # 括号不改变 AST 结构
        else:
            parser_state['error'] = "Missing closing parenthesis"
            return {
                "type": "ERROR",
                "value": "",
                "children": [],
                "line": token['line'],
                "column": token['column']
            }
    
    # 无效 token
    parser_state['error'] = f"Unexpected token '{token['value']}' at line {token['line']}, column {token['column']}"
    return {
        "type": "ERROR",
        "value": token['value'],
        "children": [],
        "line": token['line'],
        "column": token['column']
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
