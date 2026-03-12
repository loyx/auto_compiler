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
#   "filename": str,
#   "error": str,
#   "pos": int
# }

# === main function ===
def _parse_array_literal(parser_state: ParserState) -> AST:
    """
    解析数组字面量（[ ] 之间的元素列表）。
    输入：parser_state（ParserState），pos 应指向 LEFT_BRACKET。
    输出：ARRAY_LITERAL AST 节点，children 包含所有元素 AST。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查 pos 越界
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input while parsing array literal")
    
    # 1. 消费 LEFT_BRACKET token
    current_token = tokens[pos]
    if current_token["type"] != "LEFT_BRACKET":
        raise SyntaxError(f"Expected LEFT_BRACKET, got {current_token['type']}")
    
    start_line = current_token["line"]
    start_column = current_token["column"]
    parser_state["pos"] = pos + 1
    
    elements = []
    
    # 2. 检查是否立即遇到 RIGHT_BRACKET（空数组）
    pos = parser_state["pos"]
    if pos < len(tokens) and tokens[pos]["type"] == "RIGHT_BRACKET":
        # 空数组 []
        parser_state["pos"] = pos + 1
        return {
            "type": "ARRAY_LITERAL",
            "children": [],
            "value": None,
            "line": start_line,
            "column": start_column
        }
    
    # 3. 循环解析元素
    while True:
        # 解析当前元素
        element_ast = _parse_expression(parser_state)
        elements.append(element_ast)
        
        # 检查下一个 token
        pos = parser_state["pos"]
        if pos >= len(tokens):
            raise SyntaxError("Unexpected end of input while parsing array literal")
        
        next_token = tokens[pos]
        
        if next_token["type"] == "COMMA":
            # 消费 COMMA 并继续
            parser_state["pos"] = pos + 1
        elif next_token["type"] == "RIGHT_BRACKET":
            # 结束循环
            break
        else:
            raise SyntaxError(f"Expected COMMA or RIGHT_BRACKET, got {next_token['type']}")
    
    # 4. 消费 RIGHT_BRACKET
    parser_state["pos"] = pos + 1
    
    # 5. 返回 ARRAY_LITERAL AST 节点
    return {
        "type": "ARRAY_LITERAL",
        "children": elements,
        "value": None,
        "line": start_line,
        "column": start_column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function