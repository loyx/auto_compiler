# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this helper function

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
def _is_additive_operator(parser_state: ParserState) -> bool:
    """
    检查当前 token 是否为加法运算符 (PLUS/MINUS)。
    
    输入：parser_state 包含 tokens 列表和当前位置 pos
    输出：True 如果当前 token 是加法运算符，否则 False
    不修改 parser_state，仅做检查。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 如果 pos 超出 tokens 范围，返回 False
    if pos < 0 or pos >= len(tokens):
        return False
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    
    # 检查 token['type'] 是否为 "PLUS" 或 "MINUS"
    return token_type in ("PLUS", "MINUS")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function