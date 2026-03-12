# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple token consumption

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
#   "error": str | None
# }

# === main function ===
def _consume_token(parser_state: ParserState, expected_type: str | None = None) -> Token:
    """
    消费当前 token 并推进 parser_state['pos']。
    
    行为：
    1. 获取当前 token（parser_state['tokens'][parser_state['pos']]）
    2. 若 expected_type 不为 None 且当前 token['type'] != expected_type，抛出 SyntaxError
    3. 推进 parser_state['pos'] += 1
    4. 返回被消费的 token
    
    参数:
        parser_state: 解析器状态，包含 tokens 列表和当前位置 pos
        expected_type: 期望的 token 类型。若不为 None 且当前 token 类型不匹配，抛出 SyntaxError
    
    返回:
        被消费的 token
        
    异常:
        SyntaxError: 当 pos 超出 tokens 范围，或 expected_type 不匹配时抛出
    """
    # 检查 pos 是否在有效范围内
    if parser_state['pos'] >= len(parser_state['tokens']):
        raise SyntaxError("Unexpected end of file")
    
    # 获取当前 token
    current_token = parser_state['tokens'][parser_state['pos']]
    
    # 验证 token 类型（如果指定了 expected_type）
    if expected_type is not None:
        actual_type = current_token.get('type')
        if actual_type != expected_type:
            line = current_token.get('line', 0)
            column = current_token.get('column', 0)
            raise SyntaxError(
                f"Expected {expected_type} but got {actual_type} at line {line}, column {column}"
            )
    
    # 推进解析器位置
    parser_state['pos'] += 1
    
    # 返回被消费的 token
    return current_token

# === helper functions ===
# No helper functions needed for this simple function

# === OOP compatibility layer ===
# No OOP wrapper needed for this pure function