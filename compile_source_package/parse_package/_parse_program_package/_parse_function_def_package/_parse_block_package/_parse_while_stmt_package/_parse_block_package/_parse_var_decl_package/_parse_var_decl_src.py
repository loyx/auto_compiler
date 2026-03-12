# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
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
def _parse_var_decl(parser_state: ParserState) -> AST:
    """解析变量声明语句：var 标识符 = 表达式; 或 var 标识符;"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查当前位置是否有 token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input while parsing variable declaration")
    
    # 获取当前 token（应该是 VAR 关键字）
    current_token = tokens[pos]
    start_line = current_token.get("line", 0)
    start_column = current_token.get("column", 0)
    
    # 1. 消费 VAR 关键字
    parser_state = _consume_token(parser_state, "VAR")
    
    # 2. 解析标识符
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Expected identifier after 'var' keyword")
    
    identifier_token = tokens[pos]
    if identifier_token.get("type") != "IDENTIFIER":
        raise SyntaxError(f"Expected identifier, got {identifier_token.get('type')}")
    
    # 创建标识符 AST 节点
    identifier_node: AST = {
        "type": "IDENTIFIER",
        "value": identifier_token.get("value"),
        "line": identifier_token.get("line", 0),
        "column": identifier_token.get("column", 0)
    }
    
    # 消费标识符 token
    parser_state = _consume_token(parser_state, "IDENTIFIER")
    
    # 3. 检查是否有赋值运算符 =
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    init_expression_node: AST = None  # type: ignore
    
    if pos < len(tokens) and tokens[pos].get("type") == "ASSIGN":
        # 消费 = 运算符
        parser_state = _consume_token(parser_state, "ASSIGN")
        
        # 4. 解析初始化表达式
        init_expression_node = _parse_expression(parser_state)
        
        # 更新 parser_state
        parser_state = init_expression_node.get("_parser_state", parser_state)  # type: ignore
    
    # 5. 消费分号 ;
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Expected ';' at end of variable declaration")
    
    semicolon_token = tokens[pos]
    if semicolon_token.get("type") != "SEMICOLON":
        raise SyntaxError(f"Expected ';', got {semicolon_token.get('type')}")
    
    parser_state = _consume_token(parser_state, "SEMICOLON")
    
    # 构建 VAR_DECL AST 节点
    children = [identifier_node]
    if init_expression_node is not None:
        children.append(init_expression_node)
    
    result: AST = {
        "type": "VAR_DECL",
        "children": children,
        "line": start_line,
        "column": start_column
    }
    
    return result

# === helper functions ===

# === OOP compatibility layer ===
