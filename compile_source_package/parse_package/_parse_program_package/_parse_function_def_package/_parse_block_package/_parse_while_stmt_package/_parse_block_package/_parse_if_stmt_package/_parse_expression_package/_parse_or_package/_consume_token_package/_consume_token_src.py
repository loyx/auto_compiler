# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _consume_token(parser_state: ParserState, token_type: str) -> Optional[Token]:
    """
    消耗指定类型的 token。
    
    成功时更新 parser_state["pos"] 并返回 token 字典；
    失败时设置 parser_state["error"] 并返回 None。
    
    Resource effects:
    - 读取 parser_state["tokens"], parser_state["pos"]
    - 写入 parser_state["pos"], parser_state["error"]
    """
    tokens = parser_state.get("tokens")
    pos = parser_state.get("pos", 0)
    
    # 检查 tokens 是否存在或为空
    if not tokens:
        parser_state["error"] = "No tokens available"
        return None
    
    # 检查是否已到达 token 列表末尾
    if pos >= len(tokens):
        parser_state["error"] = f"Unexpected end of input, expected '{token_type}'"
        return None
    
    current_token = tokens[pos]
    actual_type = current_token.get("type", "")
    
    # 检查 token 类型是否匹配
    if actual_type == token_type:
        parser_state["pos"] = pos + 1
        return current_token
    else:
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        parser_state["error"] = f"Expected token type '{token_type}', got '{actual_type}' at line {line}, column {column}"
        return None

# === helper functions ===

# === OOP compatibility layer ===
