# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._create_ast_node_package._create_ast_node_src import _create_ast_node

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
def _parse_property(parser_state: ParserState) -> AST:
    """解析单个对象属性（key: value 对），返回 Property AST 节点。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. 检查 pos 越界
    if pos >= len(tokens):
        raise ValueError("Unexpected end of input while parsing property key")
    
    # 2. 获取当前 token 作为键 token
    key_token = tokens[pos]
    
    # 3. 验证键 token 类型是否为 STRING 或 IDENTIFIER
    if key_token["type"] not in ("STRING", "IDENTIFIER"):
        raise ValueError(
            f"Expected property key (STRING or IDENTIFIER), "
            f"got {key_token['type']} at line {key_token['line']}, column {key_token['column']}"
        )
    
    # 4. 记录键的值和位置信息
    key_line = key_token["line"]
    key_column = key_token["column"]
    
    # 创建键的 AST 节点
    key_ast = _create_ast_node(
        node_type="Identifier" if key_token["type"] == "IDENTIFIER" else "StringLiteral",
        value=key_token["value"],
        children=[],
        line=key_line,
        column=key_column
    )
    
    # 5. 消耗 COLON token
    _consume_token(parser_state, "COLON")
    
    # 6. 调用 _parse_expression 解析值表达式
    value_ast = _parse_expression(parser_state)
    
    # 7. 创建并返回 property AST 节点
    property_ast = _create_ast_node(
        node_type="Property",
        value=None,
        children=[key_ast, value_ast],
        line=key_line,
        column=key_column
    )
    
    return property_ast

# === helper functions ===
# No helper functions needed; all logic is in main function

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser helper function
