# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_params_package._parse_params_src import _parse_params
from ._parse_type_annotation_package._parse_type_annotation_src import _parse_type_annotation
from ._parse_block_package._parse_block_src import _parse_block

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
def _parse_def_statement(parser_state: ParserState) -> AST:
    """解析函数定义语句。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. 消费 DEF token
    if pos >= len(tokens) or tokens[pos]["type"] != "DEF":
        raise SyntaxError("Expected 'def' keyword")
    def_token = tokens[pos]
    pos += 1
    
    # 2. 解析函数名（IDENT token）
    if pos >= len(tokens) or tokens[pos]["type"] != "IDENT":
        raise SyntaxError("Expected function name after 'def'")
    name_token = tokens[pos]
    pos += 1
    name_node = {"type": "NAME", "value": name_token["value"], "line": name_token["line"], "column": name_token["column"]}
    
    # 3. 消费左括号 LPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "LPAREN":
        raise SyntaxError("Expected '(' after function name")
    pos += 1
    
    # 4. 解析参数列表（可选）
    params_node = {"type": "PARAMS", "children": [], "line": def_token["line"], "column": def_token["column"]}
    if pos < len(tokens) and tokens[pos]["type"] != "RPAREN":
        params_node = _parse_params(parser_state)
        pos = parser_state["pos"]
    
    # 5. 消费右括号 RPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "RPAREN":
        raise SyntaxError("Expected ')' after parameters")
    pos += 1
    
    # 6. 解析返回类型注解（可选，ARROW 后跟类型）
    return_type_node = None
    if pos < len(tokens) and tokens[pos]["type"] == "ARROW":
        pos += 1
        return_type_node = _parse_type_annotation(parser_state)
        pos = parser_state["pos"]
    
    # 7. 消费 COLON token
    if pos >= len(tokens) or tokens[pos]["type"] != "COLON":
        raise SyntaxError("Expected ':' after function signature")
    pos += 1
    
    # 8. 解析函数体 block
    if pos >= len(tokens):
        raise SyntaxError("Expected function body after ':'")
    body_node = _parse_block(parser_state)
    pos = parser_state["pos"]
    
    # 9. 消费结束分号 SEMICOLON
    if pos >= len(tokens) or tokens[pos]["type"] != "SEMICOLON":
        raise SyntaxError("Expected ';' after function definition")
    pos += 1
    
    # 更新 parser_state pos
    parser_state["pos"] = pos
    
    # 构建 DEF_STMT AST 节点
    children = [name_node, params_node]
    if return_type_node:
        children.append(return_type_node)
    children.append(body_node)
    
    return {
        "type": "DEF_STMT",
        "line": def_token["line"],
        "column": def_token["column"],
        "children": children
    }

# === helper functions ===

# === OOP compatibility layer ===
