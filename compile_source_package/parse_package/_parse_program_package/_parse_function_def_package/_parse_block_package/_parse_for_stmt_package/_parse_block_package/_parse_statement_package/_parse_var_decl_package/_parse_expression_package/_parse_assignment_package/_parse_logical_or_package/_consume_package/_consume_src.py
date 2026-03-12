# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed - directly access tokens[pos]

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
def _consume(parser_state: ParserState, expected_type: str) -> Token:
    """
    消耗当前 token 并验证类型。
    
    获取当前 token，验证其类型是否匹配 expected_type。
    如果匹配则消耗该 token（pos 加 1）并返回。
    如果不匹配或已到达输入末尾，则抛出异常。
    
    副作用：原地修改 parser_state["pos"]
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否已到达输入末尾
    if pos >= len(tokens):
        raise ValueError(f"Unexpected end of input at {parser_state.get('filename', 'unknown')}")
    
    current_token = tokens[pos]
    
    # 验证 token 类型
    if current_token["type"] != expected_type:
        raise ValueError(
            f"Unexpected token '{current_token['value']}' of type '{current_token['type']}', "
            f"expected '{expected_type}' at line {current_token.get('line', '?')}, "
            f"column {current_token.get('column', '?')}"
        )
    
    # 消耗 token：pos 加 1
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function
