# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
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
def _parse_if_stmt(parser_state: ParserState) -> AST:
    """解析 if 语句，构建 IF AST 节点。
    
    语法：if_stmt := IF LPAREN expression RPAREN block (ELSE block)?
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. 消费 IF 关键字
    if pos >= len(tokens) or tokens[pos]["type"] != "IF":
        raise SyntaxError("Expected IF keyword")
    if_line = tokens[pos]["line"]
    if_column = tokens[pos]["column"]
    pos += 1
    
    # 2. 消费 LPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "LPAREN":
        raise SyntaxError(f"Expected '(' at line {tokens[pos]['line'] if pos < len(tokens) else 'EOF'}")
    pos += 1
    
    # 3. 解析条件表达式
    condition_ast = _parse_expression(parser_state)
    pos = parser_state["pos"]
    
    # 4. 消费 RPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "RPAREN":
        raise SyntaxError(f"Expected ')' at line {tokens[pos]['line'] if pos < len(tokens) else 'EOF'}")
    pos += 1
    
    # 5. 消费 COLON（块起始标记）
    if pos >= len(tokens) or tokens[pos]["type"] != "COLON":
        raise SyntaxError(f"Expected ':' at line {tokens[pos]['line'] if pos < len(tokens) else 'EOF'}")
    pos += 1
    parser_state["pos"] = pos
    
    # 6. 解析 then 分支语句块
    then_block_ast = _parse_block(parser_state)
    pos = parser_state["pos"]
    
    # 7. 检查是否有 ELSE 分支
    children = [condition_ast, then_block_ast]
    if pos < len(tokens) and tokens[pos]["type"] == "ELSE":
        pos += 1
        # 消费 ELSE 后的 COLON
        if pos >= len(tokens) or tokens[pos]["type"] != "COLON":
            raise SyntaxError(f"Expected ':' after ELSE at line {tokens[pos]['line'] if pos < len(tokens) else 'EOF'}")
        pos += 1
        parser_state["pos"] = pos
        # 解析 else 分支语句块
        else_block_ast = _parse_block(parser_state)
        children.append(else_block_ast)
        pos = parser_state["pos"]
    
    # 8. 构建 IF AST 节点
    if_ast = {
        "type": "IF",
        "line": if_line,
        "column": if_column,
        "children": children
    }
    
    parser_state["pos"] = pos
    return if_ast


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function
