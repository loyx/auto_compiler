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
    """
    解析 if 语句。语法：if ( 条件 ) 语句块 [else 语句块]
    输入 parser_state（pos 指向 IF token），返回 IF_STMT AST 节点。
    原地更新 pos 到语句结束。语法错误抛出 SyntaxError。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # 步骤 1: 当前 token 必须是 IF
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: 预期 IF 关键字，但已到达文件末尾")
    
    if_token = tokens[pos]
    if if_token["type"] != "IF":
        raise SyntaxError(f"{filename}:{if_token['line']}:{if_token['column']}: 预期 IF 关键字，得到 {if_token['type']}")
    
    line = if_token["line"]
    column = if_token["column"]
    
    # 步骤 2: 消耗 IF token
    pos += 1
    
    # 步骤 3: 下一个 token 必须是 LPAREN
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{line}:{column}: 预期 '('，但已到达文件末尾")
    
    lparen_token = tokens[pos]
    if lparen_token["type"] != "LPAREN":
        raise SyntaxError(f"{filename}:{lparen_token['line']}:{lparen_token['column']}: 预期 '('，得到 {lparen_token['type']}")
    
    # 消耗 LPAREN
    pos += 1
    
    # 步骤 4: 解析条件表达式
    parser_state["pos"] = pos
    condition_ast = _parse_expression(parser_state)
    pos = parser_state["pos"]
    
    # 步骤 5: 下一个 token 必须是 RPAREN
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{line}:{column}: 预期 ')'，但已到达文件末尾")
    
    rparen_token = tokens[pos]
    if rparen_token["type"] != "RPAREN":
        raise SyntaxError(f"{filename}:{rparen_token['line']}:{rparen_token['column']}: 预期 ')'，得到 {rparen_token['type']}")
    
    # 消耗 RPAREN
    pos += 1
    
    # 步骤 6: 解析 then 分支语句块
    parser_state["pos"] = pos
    then_branch_ast = _parse_block(parser_state)
    pos = parser_state["pos"]
    
    # 步骤 7: 可选 else 分支
    else_branch_ast = None
    if pos < len(tokens) and tokens[pos]["type"] == "ELSE":
        # 消耗 ELSE token
        pos += 1
        # 解析 else 分支语句块
        parser_state["pos"] = pos
        else_branch_ast = _parse_block(parser_state)
        pos = parser_state["pos"]
    
    # 步骤 8: 返回 IF_STMT AST 节点
    children = [condition_ast, then_branch_ast]
    if else_branch_ast is not None:
        children.append(else_branch_ast)
    
    result = {
        "type": "IF_STMT",
        "children": children,
        "value": None,
        "line": line,
        "column": column
    }
    
    parser_state["pos"] = pos
    return result

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function