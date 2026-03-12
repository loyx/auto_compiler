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
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_assign_stmt(parser_state: ParserState) -> AST:
    """
    解析赋值语句。
    语法：IDENTIFIER ASSIGN expression SEMICOLON
    输出：ASSIGN AST 节点，包含 target（IDENTIFIER AST）和 value（expression AST）
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 步骤 1: 检查当前 token 是否为标识符
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:???: 预期标识符，但到达文件末尾")
    
    current_token = tokens[pos]
    if current_token["type"] != "IDENTIFIER":
        raise SyntaxError(
            f"{filename}:{current_token['line']}:{current_token['column']}: "
            f"预期标识符，但得到 '{current_token['value']}'"
        )
    
    # 记录标识符位置信息
    identifier_line = current_token["line"]
    identifier_column = current_token["column"]
    identifier_value = current_token["value"]
    
    # 步骤 2: 消费标识符 token
    parser_state["pos"] += 1
    pos = parser_state["pos"]
    
    # 步骤 3: 检查并消费 ASSIGN token
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{identifier_line}:{identifier_column}: 预期 '='，但到达文件末尾")
    
    assign_token = tokens[pos]
    if assign_token["type"] != "ASSIGN":
        raise SyntaxError(
            f"{filename}:{assign_token['line']}:{assign_token['column']}: "
            f"预期 '='，但得到 '{assign_token['value']}'"
        )
    
    # 消费 ASSIGN token
    parser_state["pos"] += 1
    
    # 步骤 4: 解析右侧表达式（委托给子函数）
    value_ast = _parse_expression(parser_state)
    
    # 步骤 5: 检查并消费 SEMICOLON token
    pos = parser_state["pos"]
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:???: 预期 ';'，但到达文件末尾")
    
    semicolon_token = tokens[pos]
    if semicolon_token["type"] != "SEMICOLON":
        raise SyntaxError(
            f"{filename}:{semicolon_token['line']}:{semicolon_token['column']}: "
            f"预期 ';'，但得到 '{semicolon_token['value']}'"
        )
    
    # 消费 SEMICOLON token
    parser_state["pos"] += 1
    
    # 步骤 6: 构建 IDENTIFIER AST 节点（target）
    target_ast = {
        "type": "IDENTIFIER",
        "value": identifier_value,
        "line": identifier_line,
        "column": identifier_column
    }
    
    # 步骤 7: 构建 ASSIGN AST 节点
    assign_ast = {
        "type": "ASSIGN",
        "target": target_ast,
        "value": value_ast,
        "line": identifier_line,
        "column": identifier_column
    }
    
    return assign_ast

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# Not required for parser module