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
    """解析数组字面量 [元素1, 元素2, ...]"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 1. 验证当前 token 是 '['
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}: Unexpected end of input, expected '['")
    
    current_token = tokens[pos]
    if current_token.get("type") != "LBRACKET":
        raise SyntaxError(f"{filename}: Expected '[' at line {current_token.get('line', '?')}, column {current_token.get('column', '?')}")
    
    # 2. 消费 '[' token
    start_line = current_token.get("line")
    start_column = current_token.get("column")
    pos += 1
    
    # 3. 检查是否为空数组
    elements = []
    if pos < len(tokens) and tokens[pos].get("type") == "RBRACKET":
        # 空数组 []
        pos += 1
    else:
        # 4. 解析元素列表
        while True:
            # 解析表达式作为元素
            element_ast = _parse_expression(parser_state)
            elements.append(element_ast)
            
            # 更新 pos 为子函数解析后的位置
            pos = parser_state["pos"]
            
            # 检查下一个 token
            if pos >= len(tokens):
                raise SyntaxError(f"{filename}: Unexpected end of input, expected ']' or ','")
            
            next_token = tokens[pos]
            
            # 5. 检查是否有 ','
            if next_token.get("type") == "COMMA":
                # 有逗号，消费它并继续
                pos += 1
                parser_state["pos"] = pos
            elif next_token.get("type") == "RBRACKET":
                # 无逗号，遇到 ']'，退出循环
                break
            else:
                raise SyntaxError(f"{filename}: Expected ',' or ']' at line {next_token.get('line', '?')}, column {next_token.get('column', '?')}")
        
        # 6. 消费 ']' token
        if pos >= len(tokens) or tokens[pos].get("type") != "RBRACKET":
            raise SyntaxError(f"{filename}: Expected ']' to close array literal")
        pos += 1
    
    # 更新 parser_state 的 pos
    parser_state["pos"] = pos
    
    # 7. 构建数组 AST 节点
    ast_node: AST = {
        "type": "ArrayLiteral",
        "elements": elements,
        "line": start_line,
        "column": start_column
    }
    
    return ast_node


# === helper functions ===
# No helper functions needed - logic is in main function


# === OOP compatibility layer ===
# Not needed - this is a parser utility function