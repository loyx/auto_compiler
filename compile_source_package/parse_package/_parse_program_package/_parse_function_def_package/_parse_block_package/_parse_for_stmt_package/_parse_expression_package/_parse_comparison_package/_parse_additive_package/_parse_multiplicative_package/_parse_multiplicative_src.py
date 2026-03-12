# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
import sys
import os
_unary_path = os.path.join(os.path.dirname(__file__), '_parse_unary_package', '_parse_unary_src.py')
if os.path.exists(_unary_path):
    import importlib.util
    _spec = importlib.util.spec_from_file_location('_parse_unary_src', _unary_path)
    _parse_unary_module = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_parse_unary_module)
    _parse_unary = _parse_unary_module._parse_unary
else:
    raise ImportError(f"Cannot find _parse_unary at {_unary_path}")

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
def _parse_multiplicative(parser_state: dict) -> dict:
    """解析乘法表达式（*、/）。
    
    语法：unary_expr (mul_op unary_expr)*
    乘法运算符 token 类型：MUL (*)、DIV (/)
    
    输入：parser_state，当前位置指向表达式起始 token
    输出：乘法表达式的 AST 节点，更新 parser_state['pos'] 越过表达式
    """
    # 1. 解析左侧操作数（一元表达式）
    left = _parse_unary(parser_state)
    
    # 检查是否有错误
    if parser_state.get("error"):
        return left
    
    # 2. 循环处理乘法运算符
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    while pos < len(tokens):
        current_token = tokens[pos]
        token_type = current_token.get("type", "")
        
        # 检查是否为乘法运算符
        if token_type not in ("MUL", "DIV"):
            break
        
        # 记录运算符并消费 token
        op_string = "*" if token_type == "MUL" else "/"
        parser_state["pos"] = pos + 1
        pos = parser_state["pos"]
        
        # 3. 解析右侧操作数（一元表达式）
        right = _parse_unary(parser_state)
        
        # 检查是否有错误
        if parser_state.get("error"):
            return left
        
        # 4. 构建 BINARY_OP 节点（左结合）
        left = {
            "type": "BINARY_OP",
            "value": op_string,
            "children": [left, right],
            "line": left.get("line", current_token.get("line", 0)),
            "column": left.get("column", current_token.get("column", 0))
        }
        
        # 更新位置
        pos = parser_state["pos"]
    
    # 5. 返回最终的 AST 节点
    return left

# === helper functions ===
# 无额外 helper 函数

# === OOP compatibility layer ===
# 本模块为普通函数节点，无需 OOP wrapper