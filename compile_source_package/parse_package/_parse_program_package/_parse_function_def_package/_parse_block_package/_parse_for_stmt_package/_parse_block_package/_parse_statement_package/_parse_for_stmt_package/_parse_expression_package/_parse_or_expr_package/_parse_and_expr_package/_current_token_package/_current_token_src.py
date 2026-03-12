# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# (none)

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
    """
    获取解析器当前位置的 token。
    
    若 pos 在 tokens 范围内，返回 tokens[pos]；
    若 pos 超出范围，返回 EOF token（type="EOF", value="", line=0, column=0）。
    
    副作用：无（不修改 parser_state）
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos < len(tokens):
        return tokens[pos]
    else:
        return {
            "type": "EOF",
            "value": "",
            "line": 0,
            "column": 0
        }

# === helper functions ===
# (none)

# === OOP compatibility layer ===
# (none - utility function, no framework wrapper needed)