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
def _is_at_end(parser_state: ParserState) -> bool:
    """
    检查解析器是否已到达 token 流末尾。
    
    Args:
        parser_state: 解析器状态字典，包含 tokens、pos、filename 等字段
        
    Returns:
        bool: True 表示已到达末尾（没有更多 token 需要解析），
              False 表示还有更多 token 需要解析
    """
    return parser_state["pos"] >= len(parser_state["tokens"])

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function