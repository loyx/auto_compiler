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
def _parse_tuple_literal(parser_state: ParserState) -> AST:
    """
    解析元组字面量或括号表达式。
    
    入口时 parser_state["pos"] 应指向 LEFT_PAREN token。
    出口时 pos 推进到 RIGHT_PAREN 之后。
    返回 TUPLE_LITERAL AST 节点，children 包含所有元素表达式。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "unknown")
    
    # 1. 验证并消耗 LEFT_PAREN
    if pos >= len(tokens):
        raise SyntaxError(
            f"Unexpected end of file while parsing tuple at {filename}"
        )
    
    token = tokens[pos]
    token_type = token.get("type", "")
    
    if token_type != "LEFT_PAREN":
        raise SyntaxError(
            f"Expected LEFT_PAREN but got '{token_type}' at line {token.get('line', '?')}, "
            f"column {token.get('column', '?')} in {filename}"
        )
    
    # 记录起始位置用于 AST 的 line/column
    start_line = token.get("line", 0)
    start_column = token.get("column", 0)
    
    # 消耗 LEFT_PAREN
    parser_state["pos"] = pos + 1
    pos = parser_state["pos"]
    
    # 2. 解析元素列表
    children = []
    
    # 检查是否为空元组
    if pos < len(tokens) and tokens[pos].get("type") == "RIGHT_PAREN":
        # 空元组 ()
        parser_state["pos"] = pos + 1
        return {
            "type": "TUPLE_LITERAL",
            "children": [],
            "line": start_line,
            "column": start_column
        }
    
    # 解析第一个元素
    first_child = _parse_expression(parser_state)
    children.append(first_child)
    
    pos = parser_state["pos"]
    
    # 检查是否有逗号（区分单元素元组 vs 括号表达式）
    has_trailing_comma = False
    
    if pos < len(tokens) and tokens[pos].get("type") == "COMMA":
        has_trailing_comma = True
        parser_state["pos"] = pos + 1
        pos = parser_state["pos"]
        
        # 继续解析更多元素
        while pos < len(tokens):
            token = tokens[pos]
            token_type = token.get("type", "")
            
            if token_type == "RIGHT_PAREN":
                break
            
            if token_type == "COMMA":
                # 允许尾随逗号
                parser_state["pos"] = pos + 1
                pos = parser_state["pos"]
                continue
            
            # 解析下一个元素
            child = _parse_expression(parser_state)
            children.append(child)
            pos = parser_state["pos"]
    
    # 3. 消耗 RIGHT_PAREN
    if pos >= len(tokens):
        raise SyntaxError(
            f"Unexpected end of file while parsing tuple at {filename}"
        )
    
    token = tokens[pos]
    token_type = token.get("type", "")
    
    if token_type != "RIGHT_PAREN":
        raise SyntaxError(
            f"Expected RIGHT_PAREN but got '{token_type}' at line {token.get('line', '?')}, "
            f"column {token.get('column', '?')} in {filename}"
        )
    
    parser_state["pos"] = pos + 1
    
    # 4. 返回 AST
    return {
        "type": "TUPLE_LITERAL",
        "children": children,
        "line": start_line,
        "column": start_column
    }


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this parser function
