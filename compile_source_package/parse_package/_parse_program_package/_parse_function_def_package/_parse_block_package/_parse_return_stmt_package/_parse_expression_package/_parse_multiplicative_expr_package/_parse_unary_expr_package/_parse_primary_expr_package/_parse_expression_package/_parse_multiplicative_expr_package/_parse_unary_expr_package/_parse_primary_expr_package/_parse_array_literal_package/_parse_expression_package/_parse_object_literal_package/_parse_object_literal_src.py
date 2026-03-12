# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._create_ast_node_package._create_ast_node_src import _create_ast_node
from ._parse_property_package._parse_property_src import _parse_property

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
def _parse_object_literal(parser_state: ParserState) -> AST:
    """解析对象字面量 {...}，返回 ObjectLiteral AST 节点。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查边界
    if pos >= len(tokens):
        raise ValueError(f"Unexpected end of input while parsing object literal in {parser_state.get('filename', 'unknown')}")
    
    # 1. 消耗 LEFT_BRACE token
    left_brace = _consume_token(parser_state, "LEFT_BRACE")
    start_line = left_brace["line"]
    start_column = left_brace["column"]
    
    # 2. 创建 properties 列表
    properties = []
    
    # 3. 循环解析属性直到 RIGHT_BRACE
    while True:
        # 检查是否越界
        if parser_state["pos"] >= len(tokens):
            raise ValueError(f"Unexpected end of input while parsing object literal in {parser_state.get('filename', 'unknown')}")
        
        current_token = tokens[parser_state["pos"]]
        
        # 检查是否为 RIGHT_BRACE（结束或空对象）
        if current_token["type"] == "RIGHT_BRACE":
            break
        
        # 解析属性
        property_node = _parse_property(parser_state)
        properties.append(property_node)
        
        # 检查逗号或结束
        if parser_state["pos"] >= len(tokens):
            raise ValueError(f"Unexpected end of input while parsing object literal in {parser_state.get('filename', 'unknown')}")
        
        next_token = tokens[parser_state["pos"]]
        
        if next_token["type"] == "COMMA":
            _consume_token(parser_state, "COMMA")
        elif next_token["type"] == "RIGHT_BRACE":
            break
        else:
            raise ValueError(f"Expected COMMA or RIGHT_BRACE, got {next_token['type']} at line {next_token['line']}, column {next_token['column']} in {parser_state.get('filename', 'unknown')}")
    
    # 4. 消耗 RIGHT_BRACE token
    right_brace = _consume_token(parser_state, "RIGHT_BRACE")
    
    # 5. 返回 AST 节点
    return _create_ast_node(
        node_type="ObjectLiteral",
        value=None,
        children=properties,
        line=start_line,
        column=start_column
    )

# === helper functions ===

# === OOP compatibility layer ===
