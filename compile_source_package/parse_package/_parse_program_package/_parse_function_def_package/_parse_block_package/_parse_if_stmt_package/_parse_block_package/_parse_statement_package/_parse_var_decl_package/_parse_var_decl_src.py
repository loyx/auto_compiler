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
def _parse_var_decl(parser_state: dict) -> dict:
    """
    解析变量声明语句（var x = 5; 或 let x: int = 5;）。
    输入：parser_state（pos 指向 VAR/LET 关键字）。
    输出：VAR_DECL AST 节点。
    直接修改 parser_state["pos"]。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Step 1: 消费 VAR 或 LET 关键字
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input, expected VAR or LET")
    
    keyword_token = tokens[pos]
    if keyword_token["type"] not in ("VAR", "LET"):
        raise SyntaxError(
            f"{filename}:{keyword_token['line']}:{keyword_token['column']}: "
            f"Expected VAR or LET, got {keyword_token['type']}"
        )
    
    keyword_type = keyword_token["value"]  # "var" or "let"
    ast_line = keyword_token["line"]
    ast_column = keyword_token["column"]
    parser_state["pos"] += 1
    pos = parser_state["pos"]
    
    # Step 2: 消费标识符
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input, expected identifier")
    
    ident_token = tokens[pos]
    if ident_token["type"] != "IDENTIFIER":
        raise SyntaxError(
            f"{filename}:{ident_token['line']}:{ident_token['column']}: "
            f"Expected identifier, got {ident_token['type']}"
        )
    
    identifier_node = {
        "type": "IDENTIFIER",
        "value": ident_token["value"],
        "line": ident_token["line"],
        "column": ident_token["column"]
    }
    parser_state["pos"] += 1
    pos = parser_state["pos"]
    
    # Step 3: 检查类型注解
    type_annotation = None
    if pos < len(tokens) and tokens[pos]["type"] == "COLON":
        parser_state["pos"] += 1
        pos = parser_state["pos"]
        
        if pos >= len(tokens):
            raise SyntaxError(f"{filename}:0:0: Unexpected end of input after colon")
        
        type_token = tokens[pos]
        if type_token["type"] not in ("INT", "STRING", "BOOL"):
            raise SyntaxError(
                f"{filename}:{type_token['line']}:{type_token['column']}: "
                f"Expected INT, STRING, or BOOL, got {type_token['type']}"
            )
        
        type_annotation = type_token["value"]
        parser_state["pos"] += 1
        pos = parser_state["pos"]
    
    # Step 4: 检查初始化表达式
    children = [identifier_node]
    if pos < len(tokens) and tokens[pos]["type"] == "ASSIGN":
        parser_state["pos"] += 1
        expr_node = _parse_expression(parser_state)
        children.append(expr_node)
        pos = parser_state["pos"]
    
    # Step 5: 消费分号
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input, expected semicolon")
    
    semicolon_token = tokens[pos]
    if semicolon_token["type"] != "SEMICOLON":
        raise SyntaxError(
            f"{filename}:{semicolon_token['line']}:{semicolon_token['column']}: "
            f"Expected semicolon, got {semicolon_token['type']}"
        )
    parser_state["pos"] += 1
    
    # Step 6: 构建 AST 节点
    ast_node: AST = {
        "type": "VAR_DECL",
        "line": ast_line,
        "column": ast_column,
        "children": children,
        "type_annotation": type_annotation
    }
    
    return ast_node

# === helper functions ===
# No helper functions needed; all logic is in main function.

# === OOP compatibility layer ===
# Not needed for this parser function.