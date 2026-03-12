# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this utility function

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (PLUS, MINUS, STAR, SLASH, PERCENT, EQ, NE, LT, GT, LE, GE, AND, OR, BANG, IDENTIFIER, INTEGER, STRING, LPAREN, RPAREN)
#   "value": str,            # token 值
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
def _expect_token(parser_state: ParserState, token_type: str) -> Token:
    """检查并消耗期望的 token 类型。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # 检查是否已到达 token 末尾
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: expected {token_type}, got EOF")
    
    current_token = tokens[pos]
    
    # 检查 token 类型是否匹配
    if current_token["type"] == token_type:
        # 消耗 token
        parser_state["pos"] = pos + 1
        return current_token
    else:
        # token 类型不匹配
        raise SyntaxError(f"{filename}:{current_token['line']}:{current_token['column']}: expected {token_type}, got {current_token['type']}")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function