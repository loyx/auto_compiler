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
def _parse_list_literal(parser_state: ParserState) -> AST:
    """
    解析列表字面量，格式为 [expr1, expr2, ...]。
    输入：parser_state（当前位置指向 '[' token）
    输出：LIST_LITERAL AST 节点，children 包含所有元素 AST
    副作用：更新 parser_state["pos"] 到 ']' 之后的位置
    错误时返回 ERROR 节点并设置 parser_state["error"]
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 验证当前 token 是 '['
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input, expected '['"
        return _make_error_node("Unexpected end of input", tokens, pos)
    
    current_token = tokens[pos]
    if current_token["type"] != "LBRACKET" and current_token["value"] != "[":
        parser_state["error"] = f"Expected '[', got {current_token['value']}"
        return _make_error_node("Expected '['", tokens, pos)
    
    # 记录起始位置
    start_line = current_token.get("line", 0)
    start_column = current_token.get("column", 0)
    
    # 跳过 '[' token
    pos += 1
    
    elements = []
    
    # 循环解析表达式
    while pos < len(tokens):
        current_token = tokens[pos]
        
        # 遇到 ']' 结束
        if current_token["type"] == "RBRACKET" or current_token["value"] == "]":
            pos += 1
            break
        
        # 解析表达式
        expr_ast = _parse_expression(parser_state)
        
        # 检查解析是否出错
        if parser_state.get("error"):
            return expr_ast
        
        elements.append(expr_ast)
        
        # 检查是否有逗号或结束
        if pos >= len(tokens):
            parser_state["error"] = "Unexpected end of input, expected ',' or ']'"
            return _make_error_node("Unexpected end of input", tokens, pos)
        
        current_token = tokens[pos]
        
        # 如果是逗号，继续下一个元素
        if current_token["type"] == "COMMA" or current_token["value"] == ",":
            pos += 1
        # 如果不是 ']' 也不是逗号，报错
        elif current_token["type"] != "RBRACKET" and current_token["value"] != "]":
            parser_state["error"] = f"Expected ',' or ']', got {current_token['value']}"
            return _make_error_node("Expected ',' or ']'", tokens, pos)
    
    # 更新 parser_state 位置
    parser_state["pos"] = pos
    
    # 构建 LIST_LITERAL AST 节点
    return {
        "type": "LIST_LITERAL",
        "children": elements,
        "value": None,
        "line": start_line,
        "column": start_column
    }

# === helper functions ===
def _make_error_node(message: str, tokens: list, pos: int) -> AST:
    """创建错误 AST 节点。"""
    line = tokens[pos].get("line", 0) if pos < len(tokens) else 0
    column = tokens[pos].get("column", 0) if pos < len(tokens) else 0
    return {
        "type": "ERROR",
        "children": [],
        "value": message,
        "line": line,
        "column": column
    }

# === OOP compatibility layer ===
# Not required for this parser function node
