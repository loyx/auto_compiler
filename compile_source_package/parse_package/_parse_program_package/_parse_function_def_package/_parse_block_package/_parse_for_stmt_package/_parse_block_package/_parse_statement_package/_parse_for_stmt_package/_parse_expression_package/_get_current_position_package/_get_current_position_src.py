# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this helper

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
def _get_current_position(parser_state: ParserState) -> tuple:
    """
    获取当前 token 的位置信息。
    
    若 parser_state["pos"] 在 tokens 范围内，返回 (tokens[pos]["line"], tokens[pos]["column"])
    若 pos 超出范围或 tokens 为空，返回 (0, 0)
    无副作用，不修改 parser_state
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 检查 tokens 是否为空或 pos 是否超出范围
    if not tokens or pos < 0 or pos >= len(tokens):
        return (0, 0)
    
    # 获取当前 token 的位置信息
    current_token = tokens[pos]
    line = current_token.get("line", 0)
    column = current_token.get("column", 0)
    
    return (line, column)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function
