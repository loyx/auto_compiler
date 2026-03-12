# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
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

DictEntry = Dict[str, Any]
# DictEntry possible fields:
# {
#   "key": AST,
#   "value": AST
# }

# === main function ===
def _parse_dict_literal(parser_state: ParserState) -> AST:
    """解析字典字面量（{ } 之间的键值对）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. 消费 LEFT_BRACE token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected '{'")
    
    current_token = tokens[pos]
    if current_token["type"] != "LEFT_BRACE":
        raise SyntaxError(f"Expected '{{', got {current_token['type']}")
    
    start_line = current_token.get("line", 0)
    start_column = current_token.get("column", 0)
    pos += 1
    
    # 2. 检查是否立即遇到 RIGHT_BRACE（空字典）
    entries = []
    
    while pos < len(tokens):
        current_token = tokens[pos]
        
        # 3. 检查是否结束
        if current_token["type"] == "RIGHT_BRACE":
            pos += 1
            break
        
        # 4. 解析 key
        key_ast = _parse_expression(parser_state)
        
        # 5. 期望并消费 COLON
        pos = parser_state["pos"]
        if pos >= len(tokens):
            raise SyntaxError("Unexpected end of input, expected ':'")
        
        current_token = tokens[pos]
        if current_token["type"] != "COLON":
            raise SyntaxError(f"Expected ':', got {current_token['type']}")
        pos += 1
        
        # 6. 解析 value
        value_ast = _parse_expression(parser_state)
        
        # 7. 创建 DictEntry 节点
        entry = {"key": key_ast, "value": value_ast}
        entries.append(entry)
        
        # 8. 检查下一个 token
        pos = parser_state["pos"]
        if pos >= len(tokens):
            raise SyntaxError("Unexpected end of input, expected '}' or ','")
        
        current_token = tokens[pos]
        if current_token["type"] == "COMMA":
            pos += 1
        elif current_token["type"] == "RIGHT_BRACE":
            pos += 1
            break
        else:
            raise SyntaxError(f"Expected ',' or '}}', got {current_token['type']}")
    
    # 9. 返回 DICT_LITERAL AST 节点
    result = {
        "type": "DICT_LITERAL",
        "children": entries,
        "value": None,
        "line": start_line,
        "column": start_column
    }
    
    parser_state["pos"] = pos
    return result

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function