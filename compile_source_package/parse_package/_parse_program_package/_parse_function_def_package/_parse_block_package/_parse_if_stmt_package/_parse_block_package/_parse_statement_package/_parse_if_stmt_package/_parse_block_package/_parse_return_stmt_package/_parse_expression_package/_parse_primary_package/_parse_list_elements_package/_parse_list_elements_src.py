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
def _parse_list_elements(parser_state: dict) -> list:
    """
    解析列表字面量中的逗号分隔表达式列表。
    
    输入：parser_state（pos 指向 LBRACKET 后的第一个 token）
    输出：AST 节点列表
    副作用：修改 parser_state["pos"] 到 RBRACKET 位置（不消费 RBRACKET）
    异常：语法错误时抛出 SyntaxError
    """
    tokens = parser_state["tokens"]
    filename = parser_state.get("filename", "<unknown>")
    elements = []
    expect_comma = False
    
    while True:
        if parser_state["pos"] >= len(tokens):
            line = tokens[-1]["line"] if tokens else 0
            column = tokens[-1]["column"] if tokens else 0
            raise SyntaxError(f"{filename}:{line}:{column}: Unexpected end of input, expected ']'")
        
        current_token = tokens[parser_state["pos"]]
        
        # Check for RBRACKET (end of list)
        if current_token["type"] == "RBRACKET":
            break
        
        # Check for COMMA
        if current_token["type"] == "COMMA":
            if expect_comma:
                # Previous iteration expected comma, got comma - this is valid
                expect_comma = False
                parser_state["pos"] += 1
                continue
            else:
                # Got comma but didn't expect it (e.g., [1,,2] or [,1])
                raise SyntaxError(
                    f"{filename}:{current_token['line']}:{current_token['column']}: "
                    "Unexpected comma in list"
                )
        
        # If we expected a comma but got something else, that's an error
        if expect_comma:
            raise SyntaxError(
                f"{filename}:{current_token['line']}:{current_token['column']}: "
                "Expected ',' before expression"
            )
        
        # Parse the expression
        ast_node = _parse_expression(parser_state)
        elements.append(ast_node)
        expect_comma = True
    
    return elements

# === helper functions ===

# === OOP compatibility layer ===
