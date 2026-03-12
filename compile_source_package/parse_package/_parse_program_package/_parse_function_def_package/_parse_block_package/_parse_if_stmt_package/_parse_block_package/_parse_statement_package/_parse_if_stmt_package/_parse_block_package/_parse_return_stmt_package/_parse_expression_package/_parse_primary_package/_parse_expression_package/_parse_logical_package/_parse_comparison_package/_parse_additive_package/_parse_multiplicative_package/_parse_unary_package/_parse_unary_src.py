# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary

# === ADT defines ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]

# === main function ===
def _parse_unary(parser_state: ParserState) -> AST:
    """
    解析一元表达式（NOT, -）。
    首先检查一元运算符，然后递归解析或调用 _parse_primary。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 检查当前位置是否为一元运算符
    if pos < len(tokens):
        current_token = tokens[pos]
        op = current_token["value"]
        
        if op in ["not", "-"]:
            # 记录运算符位置
            op_line = current_token.get("line", 0)
            op_column = current_token.get("column", 0)
            
            # 消耗运算符 token
            parser_state["pos"] = pos + 1
            
            # 解析操作数（递归调用一元解析）
            operand_ast = _parse_unary(parser_state)
            
            # 构建 UnaryOp AST 节点
            return {
                "type": "UnaryOp",
                "op": op,
                "operand": operand_ast,
                "line": op_line,
                "column": op_column
            }
    
    # 没有一元运算符，解析初级表达式
    return _parse_primary(parser_state)

# === helper functions ===

# === OOP compatibility layer ===
