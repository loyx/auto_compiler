# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this utility function

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
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
def _current_token(parser_state: ParserState) -> Token:
    """获取当前位置的 token。
    
    若 pos 在 tokens 范围内，返回 tokens[pos]。
    若 pos 超出范围，返回 EOF token。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if _is_within_range(tokens, pos):
        return tokens[pos]
    else:
        return _create_eof_token(tokens, pos)


# === helper functions ===
def _is_within_range(tokens: list, pos: int) -> bool:
    """检查位置是否在 tokens 列表有效范围内。"""
    return 0 <= pos < len(tokens)


def _create_eof_token(tokens: list, pos: int) -> Token:
    """创建 EOF token。
    
    line 和 column 取自最后一个 token（如果存在），否则为 0。
    """
    if tokens and len(tokens) > 0:
        last_token = tokens[-1]
        line = last_token.get("line", 0)
        column = last_token.get("column", 0)
    else:
        line = 0
        column = 0
    
    return {
        "type": "EOF",
        "value": "",
        "line": line,
        "column": column
    }


# === OOP compatibility layer ===
# Not needed for this utility function