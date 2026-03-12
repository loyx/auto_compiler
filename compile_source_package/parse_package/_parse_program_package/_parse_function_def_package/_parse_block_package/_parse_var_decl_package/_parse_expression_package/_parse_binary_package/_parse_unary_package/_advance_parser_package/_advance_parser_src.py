# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions

# === ADT defines ===
ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }

# === main function ===
def _advance_parser(parser_state: ParserState) -> None:
    """
    消耗当前 token，将 parser_state["pos"] 加 1。
    
    副作用：直接修改传入的 parser_state 字典的 pos 字段。
    无返回值。
    不进行边界检查（由上层调用者负责）。
    """
    parser_state["pos"] += 1

# === helper functions ===
# No helper functions

# === OOP compatibility layer ===
# Not required for this function node