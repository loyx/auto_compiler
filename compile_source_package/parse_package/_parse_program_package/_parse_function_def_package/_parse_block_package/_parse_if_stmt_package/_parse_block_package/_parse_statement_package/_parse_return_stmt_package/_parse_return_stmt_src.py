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
    解析 return 语句（return; 或 return expr;）。
    输入：parser_state（pos 指向 RETURN 关键字）。
    输出：RETURN_STMT AST 节点。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 1. 记录 RETURN 关键字的位置
    return_token = tokens[pos]
    line = return_token["line"]
    column = return_token["column"]
    
    # 2. 消费 RETURN 关键字
    pos += 1
    
    # 3. 检查是否有返回值
    children = []
    if pos < len(tokens) and tokens[pos]["type"] != "SEMICOLON":
        # 有返回值，解析表达式
        expr_ast = _parse_expression(parser_state)
        children.append(expr_ast)
        pos = parser_state["pos"]
    
    # 4. 消费 SEMICOLON
    if pos >= len(tokens) or tokens[pos]["type"] != "SEMICOLON":
        raise SyntaxError(f"{filename}:{line}:{column}: expected ';' after return statement")
    pos += 1
    
    # 更新 parser_state 位置
    parser_state["pos"] = pos
    
    # 5. 构建 RETURN_STMT AST 节点
    return {
        "type": "RETURN_STMT",
        "children": children,
        "line": line,
        "column": column
    }

# === helper functions ===
# (none needed)

# === OOP compatibility layer ===
# (not needed for parser function)
