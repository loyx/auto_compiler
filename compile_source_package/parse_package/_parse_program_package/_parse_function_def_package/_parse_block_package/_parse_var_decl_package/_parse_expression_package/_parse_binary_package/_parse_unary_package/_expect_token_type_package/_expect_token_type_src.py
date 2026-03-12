# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._get_current_token_package._get_current_token_src import _get_current_token
from ._advance_parser_package._advance_parser_src import _advance_parser

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
def _expect_token_type(parser_state: dict, expected_type: str, expected_display: str) -> None:
    """
    期望当前 token 为指定类型，否则抛出 SyntaxError。
    
    如果匹配则消耗 token（调用 _advance_parser）。
    如果不匹配则抛出 SyntaxError，包含详细的文件名、行号、列号信息。
    """
    token = _get_current_token(parser_state)
    
    if token is None or token["type"] != expected_type:
        filename = parser_state.get("filename", "<unknown>")
        line = token["line"] if token else 0
        col = token["column"] if token else 0
        actual = token["type"] if token else "EOF"
        raise SyntaxError(f"{filename}:{line}:{col}: 期望 '{expected_display}'，但得到 '{actual}'")
    
    _advance_parser(parser_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser helper function
