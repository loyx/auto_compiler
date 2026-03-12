# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._consume_token_package._consume_token_src import _consume_token
from ._current_token_package._current_token_src import _current_token

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
def _parse_list_literal(parser_state: ParserState) -> AST:
    """解析列表字面量 [...] 并返回 AST 节点。"""
    # 步骤 1: 消耗 LEFT_BRACKET
    _consume_token(parser_state, "LEFT_BRACKET")
    
    # 步骤 2: 初始化列表 AST 节点
    list_ast: AST = {
        "type": "list_literal",
        "children": [],
        "value": None,
        "line": parser_state.get("pos", 0),
        "column": 0
    }
    
    # 步骤 3: 循环解析元素
    while True:
        token = _current_token(parser_state)
        
        # 检查是否遇到 RIGHT_BRACKET
        if token is None or token.get("type") == "RIGHT_BRACKET":
            break
        
        # 解析表达式元素
        element_ast = _parse_expression(parser_state)
        list_ast["children"].append(element_ast)
        
        # 检查后续 token
        next_token = _current_token(parser_state)
        
        # 如果遇到 COMMA，继续循环
        if next_token and next_token.get("type") == "COMMA":
            _consume_token(parser_state, "COMMA")
            # 支持尾随逗号：如果逗号后直接是 RIGHT_BRACKET，退出
            after_comma = _current_token(parser_state)
            if after_comma and after_comma.get("type") == "RIGHT_BRACKET":
                break
        # 如果不是 COMMA 也不是 RIGHT_BRACKET，说明语法错误
        elif next_token and next_token.get("type") != "RIGHT_BRACKET":
            raise SyntaxError(
                f"Expected COMMA or RIGHT_BRACKET, got {next_token.get('type')} "
                f"at line {next_token.get('line')}, column {next_token.get('column')}"
            )
    
    # 步骤 4: 消耗 RIGHT_BRACKET
    _consume_token(parser_state, "RIGHT_BRACKET")
    
    # 步骤 5: 返回列表 AST 节点
    return list_ast

# === helper functions ===
# No helper functions needed - all logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed for parser function node
