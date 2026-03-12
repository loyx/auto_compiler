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

# === main function ===
def _parse_array_literal(parser_state: ParserState) -> AST:
    """解析数组字面量 [...]，返回 ArrayLiteral AST 节点。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 检查当前位置是否为 LEFT_BRACKET
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}: Unexpected end of input, expected '['")
    
    current_token = tokens[pos]
    if current_token["type"] != "LEFT_BRACKET":
        raise SyntaxError(
            f"{filename}:{current_token.get('line', '?')}:{current_token.get('column', '?')} "
            f"Expected '[', got {current_token['type']}"
        )
    
    # 记录数组起始位置
    start_line = current_token.get("line", 0)
    start_column = current_token.get("column", 0)
    
    # 消耗 LEFT_BRACKET
    pos += 1
    
    # 解析数组元素
    elements = _parse_array_elements(tokens, pos, filename)
    elements_list, pos = elements
    
    # 检查并消耗 RIGHT_BRACKET
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}: Unexpected end of input, expected ']'")
    
    closing_token = tokens[pos]
    if closing_token["type"] != "RIGHT_BRACKET":
        raise SyntaxError(
            f"{filename}:{closing_token.get('line', '?')}:{closing_token.get('column', '?')} "
            f"Expected ']', got {closing_token['type']}"
        )
    
    # 消耗 RIGHT_BRACKET
    pos += 1
    
    # 更新 parser_state 位置
    parser_state["pos"] = pos
    
    # 返回 ArrayLiteral AST 节点
    return {
        "type": "ArrayLiteral",
        "children": elements_list,
        "value": None,
        "line": start_line,
        "column": start_column
    }

# === helper functions ===
def _parse_array_elements(tokens, pos, filename):
    """解析数组元素列表，返回 (elements_list, new_pos)。"""
    elements = []
    
    while pos < len(tokens):
        current_token = tokens[pos]
        
        # 检查是否为 RIGHT_BRACKET（数组结束）
        if current_token["type"] == "RIGHT_BRACKET":
            break
        
        # 解析当前元素（递归调用 _parse_expression）
        temp_state = {"tokens": tokens, "pos": pos, "filename": filename}
        element_ast = _parse_expression(temp_state)
        elements.append(element_ast)
        pos = temp_state["pos"]
        
        # 检查后续 token
        if pos >= len(tokens):
            raise SyntaxError(f"{filename}: Unexpected end of input in array literal")
        
        next_token = tokens[pos]
        
        # 如果是 COMMA，消耗它并继续
        if next_token["type"] == "COMMA":
            pos += 1
        # 如果不是 RIGHT_BRACKET，说明格式错误
        elif next_token["type"] != "RIGHT_BRACKET":
            raise SyntaxError(
                f"{filename}:{next_token.get('line', '?')}:{next_token.get('column', '?')} "
                f"Expected ',' or ']', got {next_token['type']}"
            )
    
    return elements, pos

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function node
