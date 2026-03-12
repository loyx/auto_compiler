# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_block_package._parse_block_src import _parse_block
from ._parse_param_list_package._parse_param_list_src import _parse_param_list

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
def _parse_function_def(parser_state: dict) -> dict:
    """解析单个函数定义。
    
    输入：parser_state（当前位于函数返回类型 token）
    输出：FUNCTION_DEF 类型 AST 节点
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 1. 解析返回类型
    if pos >= len(tokens):
        raise SyntaxError(f"Syntax error at {filename}:0:0 - expected return type but reached end of file")
    return_type_token = tokens[pos]
    return_type = return_type_token["value"]
    pos += 1
    
    # 2. 解析函数名
    if pos >= len(tokens):
        raise SyntaxError(f"Syntax error at {filename}:0:0 - expected function name after return type")
    name_token = tokens[pos]
    if name_token["type"] != "IDENTIFIER":
        raise SyntaxError(f"Syntax error at {filename}:{name_token['line']}:{name_token['column']} - expected function name after return type")
    func_name = name_token["value"]
    func_line = name_token["line"]
    func_column = name_token["column"]
    pos += 1
    
    # 3. 匹配左括号 LPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "LPAREN":
        raise SyntaxError(f"Syntax error at {filename}:{func_line}:{func_column} - expected '(' after function name")
    pos += 1
    
    # 4. 解析参数列表
    params = []
    if pos < len(tokens) and tokens[pos]["type"] != "RPAREN":
        params, pos = _parse_param_list(parser_state, pos)
    
    # 5. 匹配右括号 RPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "RPAREN":
        raise SyntaxError(f"Syntax error at {filename}:{func_line}:{func_column} - expected ')' after parameter list")
    pos += 1
    
    # 6. 匹配左花括号 LBRACE
    if pos >= len(tokens) or tokens[pos]["type"] != "LBRACE":
        raise SyntaxError(f"Syntax error at {filename}:{func_line}:{func_column} - expected '{{' before function body")
    pos += 1
    
    # 更新 parser_state 位置
    parser_state["pos"] = pos
    
    # 7. 解析语句块
    body = _parse_block(parser_state)
    
    # 9. 返回 FUNCTION_DEF 节点
    return {
        "type": "FUNCTION_DEF",
        "value": func_name,
        "return_type": return_type,
        "params": params,
        "body": body,
        "line": func_line,
        "column": func_column
    }

# === helper functions ===

# === OOP compatibility layer ===
