# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (e.g., "MINUS", "PLUS", "NOT", "BANG", "IDENTIFIER", "NUMBER")
#   "value": str,            # token 值 (e.g., "-", "+", "not", "!", "x", "42")
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (UNARY_OP, BINARY_OP, IDENTIFIER, LITERAL, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值 (对于 UNARY_OP，包含 {"operator": str})
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
def _parse_unary(parser_state: dict) -> dict:
    """
    解析一元表达式（包括前缀运算符 -, +, not, ! 等）。
    输入：parser_state（Dict，ParserState 类型）
    副作用：直接修改 parser_state["pos"] 消耗 token
    返回：AST 节点（Dict）
    异常：遇到无效 token 时抛出 SyntaxError
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if we have a token to read
    if pos >= len(tokens):
        filename = parser_state.get("filename", "<unknown>")
        raise SyntaxError(f"{filename}:0:0: 期望表达式但遇到文件结束")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    # Check if current token is a unary operator
    if token_type in ("MINUS", "PLUS", "NOT", "BANG"):
        # Consume the operator token
        parser_state["pos"] += 1
        
        # Recursively parse the operand (supports chained unary ops like --x)
        operand_ast = _parse_unary(parser_state)
        
        # Build UNARY_OP node
        return {
            "type": "UNARY_OP",
            "value": {"operator": current_token["value"]},
            "children": [operand_ast],
            "line": current_token["line"],
            "column": current_token["column"]
        }
    else:
        # Not a unary operator, parse primary expression
        return _parse_primary(parser_state)

# === helper functions ===
def _is_unary_operator(token_type: str) -> bool:
    """
    判断给定的 token 类型是否为一元运算符。
    输入：token_type (str) - token 类型字符串
    返回：bool - True 如果是一元运算符
    """
    return token_type in ("MINUS", "PLUS", "NOT", "BANG")

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function node
