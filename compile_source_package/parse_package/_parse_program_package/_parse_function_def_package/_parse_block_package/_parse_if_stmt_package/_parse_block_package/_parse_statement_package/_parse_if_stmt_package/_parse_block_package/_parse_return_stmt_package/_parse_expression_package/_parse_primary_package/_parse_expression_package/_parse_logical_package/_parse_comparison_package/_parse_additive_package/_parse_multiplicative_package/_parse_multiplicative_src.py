# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_package._parse_unary_src import _parse_unary

# === ADT defines ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]

# === main function ===
def _parse_multiplicative(parser_state: ParserState) -> AST:
    """
    解析乘法表达式（*, /, %）。
    首先调用 _parse_unary 解析左侧操作数，然后检查乘法运算符。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 解析左侧操作数（一元表达式）
    left_ast = _parse_unary(parser_state)
    
    # 检查当前位置是否有乘法运算符
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        op = current_token["value"]
        
        if op not in ["*", "/", "%"]:
            break
        
        # 记录运算符位置
        op_line = current_token.get("line", 0)
        op_column = current_token.get("column", 0)
        
        # 消耗运算符 token
        parser_state["pos"] += 1
        
        # 解析右侧操作数（一元表达式）
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(f"{filename}:{op_line}:{op_column}: 乘法运算符右侧缺少表达式")
        
        right_ast = _parse_unary(parser_state)
        
        # 构建 BinaryOp AST 节点
        left_ast = {
            "type": "BinaryOp",
            "op": op,
            "left": left_ast,
            "right": right_ast,
            "line": op_line,
            "column": op_column
        }
    
    return left_ast

# === helper functions ===

# === OOP compatibility layer ===
