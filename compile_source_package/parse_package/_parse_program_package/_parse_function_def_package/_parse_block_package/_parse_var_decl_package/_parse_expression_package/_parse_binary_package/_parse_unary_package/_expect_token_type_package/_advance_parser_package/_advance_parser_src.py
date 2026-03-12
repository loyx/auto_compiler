# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple helper

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
def _advance_parser(parser_state: ParserState) -> None:
    """
    消耗当前 token，将 parser_state["pos"] 加 1。
    
    副作用：直接修改传入的 parser_state 字典，使 pos 指向下一个 token。
    边界：即使 pos 已超出 tokens 长度，仍会递增（调用者应自行处理 EOF）。
    """
    parser_state["pos"] += 1

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function