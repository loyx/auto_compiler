# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No sub functions required

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
def _get_current_token(parser_state: ParserState) -> Optional[Token]:
    """获取 parser_state 当前位置的 token。
    
    从 parser_state 中提取 tokens 列表和当前位置 pos，
    如果位置有效则返回对应 token，否则返回 None。
    纯函数，无副作用。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos < len(tokens):
        return tokens[pos]
    return None

# === helper functions ===
# No helper functions required

# === OOP compatibility layer ===
# No OOP wrapper required for this utility function