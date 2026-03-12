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
def _parse_return_stmt(parser_state: ParserState) -> AST:
    """
    解析 return 语句。
    
    return_stmt := RETURN expression? SEMICOLON
    
    输入：parser_state（pos 指向 RETURN token）
    输出：RETURN AST 节点
    副作用：消费 return 语句所有 token，更新 pos 到语句结束
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. 获取 RETURN token 并记录位置
    return_token = tokens[pos]
    line = return_token["line"]
    column = return_token["column"]
    
    # 2. 消费 RETURN token
    parser_state["pos"] += 1
    pos = parser_state["pos"]
    
    # 3. 检查是否有表达式（下一个 token 是否为 SEMICOLON）
    children = []
    if pos < len(tokens) and tokens[pos]["type"] != "SEMICOLON":
        # 有表达式，调用 _parse_expression 解析
        expr_ast = _parse_expression(parser_state)
        children.append(expr_ast)
        pos = parser_state["pos"]
    
    # 4. 检查并消费 SEMICOLON（必需）
    if pos >= len(tokens) or tokens[pos]["type"] != "SEMICOLON":
        filename = parser_state.get("filename", "unknown")
        raise SyntaxError(
            f"Missing SEMICOLON after return statement at {filename}:{line}:{column}"
        )
    
    # 消费 SEMICOLON
    parser_state["pos"] += 1
    
    # 5. 构建并返回 AST 节点
    return {
        "type": "RETURN",
        "value": None,
        "children": children,
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node