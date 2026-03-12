# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
from ._create_ast_node_package._create_ast_node_src import _create_ast_node
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
def _parse_identifier(parser_state: ParserState) -> AST:
    """解析标识符或函数调用。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 检查 pos 是否越界
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input while parsing identifier"
        return _create_ast_node("ERROR", value=None, line=0, column=0)
    
    current_token = tokens[pos]
    identifier_name = current_token.get("value", "")
    line = current_token.get("line", 0)
    column = current_token.get("column", 0)
    
    # 消费 IDENTIFIER token
    parser_state["pos"] = pos + 1
    
    # 检查下一个 token 是否为 LEFT_PAREN（函数调用）
    next_pos = parser_state.get("pos", 0)
    if next_pos < len(tokens) and tokens[next_pos].get("type") == "LEFT_PAREN":
        # 解析函数调用
        return _parse_function_call(parser_state, identifier_name, line, column)
    else:
        # 普通标识符
        return _create_ast_node("IDENTIFIER", value=identifier_name, line=line, column=column)

# === helper functions ===
def _parse_function_call(parser_state: ParserState, func_name: str, line: int, column: int) -> AST:
    """解析函数调用：已消费 IDENTIFIER，当前 pos 指向 LEFT_PAREN。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 消费 LEFT_PAREN
    parser_state["pos"] = pos + 1
    
    arguments: List[AST] = []
    
    # 检查是否为空参数列表（直接遇到 RIGHT_PAREN）
    current_pos = parser_state.get("pos", 0)
    if current_pos < len(tokens) and tokens[current_pos].get("type") == "RIGHT_PAREN":
        # 空参数列表，消费 RIGHT_PAREN
        parser_state["pos"] = current_pos + 1
        return _create_ast_node("FUNCTION_CALL", value=func_name, children=arguments, line=line, column=column)
    
    # 解析参数列表
    while True:
        current_pos = parser_state.get("pos", 0)
        
        # 检查是否越界
        if current_pos >= len(tokens):
            parser_state["error"] = "Unexpected end of input while parsing function arguments"
            return _create_ast_node("ERROR", value=func_name, line=line, column=column)
        
        current_token = tokens[current_pos]
        
        # 检查是否遇到 RIGHT_PAREN（参数列表结束）
        if current_token.get("type") == "RIGHT_PAREN":
            parser_state["pos"] = current_pos + 1
            break
        
        # 解析参数表达式（委托给_parse_expression）
        arg_ast = _parse_expression(parser_state)
        
        # 检查解析是否出错
        if parser_state.get("error"):
            return _create_ast_node("ERROR", value=func_name, line=line, column=column)
        
        arguments.append(arg_ast)
        
        # 检查下一个 token 是 COMMA 还是 RIGHT_PAREN
        next_pos = parser_state.get("pos", 0)
        if next_pos >= len(tokens):
            parser_state["error"] = "Unexpected end of input while parsing function arguments"
            return _create_ast_node("ERROR", value=func_name, line=line, column=column)
        
        next_token = tokens[next_pos]
        if next_token.get("type") == "COMMA":
            # 消费 COMMA，继续解析下一个参数
            parser_state["pos"] = next_pos + 1
        elif next_token.get("type") == "RIGHT_PAREN":
            # 参数列表结束，将在下一轮循环中处理
            continue
        else:
            parser_state["error"] = f"Expected COMMA or RIGHT_PAREN, got {next_token.get('type')}"
            return _create_ast_node("ERROR", value=func_name, line=line, column=column)
    
    return _create_ast_node("FUNCTION_CALL", value=func_name, children=arguments, line=line, column=column)

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function node
