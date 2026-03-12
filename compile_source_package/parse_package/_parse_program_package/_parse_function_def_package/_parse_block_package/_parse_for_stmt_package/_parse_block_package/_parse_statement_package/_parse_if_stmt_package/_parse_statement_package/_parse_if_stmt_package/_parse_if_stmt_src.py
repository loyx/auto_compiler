# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_block_package._parse_block_src import _parse_block
from ._expect_token_package._expect_token_src import _expect_token

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
def _parse_if_stmt(parser_state: dict) -> dict:
    """
    解析 if 语句。
    语法：if ( expression ) block [ else block ]
    输入：parser_state（pos 指向 IF token）
    输出：IF_STMT AST 节点
    副作用：更新 pos 到 if 语句结束
    异常：语法错误抛出 SyntaxError
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 获取 IF token 的位置信息
    if_token = tokens[pos]
    line = if_token["line"]
    column = if_token["column"]
    
    # 1. 消耗 IF token
    parser_state["pos"] += 1
    
    # 2. 消耗 LPAREN token
    _expect_token(parser_state, "LPAREN")
    
    # 3. 解析条件表达式
    condition_ast = _parse_expression(parser_state)
    
    # 4. 消耗 RPAREN token
    _expect_token(parser_state, "RPAREN")
    
    # 5. 解析 then 分支代码块
    then_block_ast = _parse_block(parser_state)
    
    # 6. 检查是否有 else 分支
    children = [condition_ast, then_block_ast]
    pos = parser_state["pos"]
    if pos < len(tokens) and tokens[pos]["type"] == "ELSE":
        # 消耗 ELSE token
        parser_state["pos"] += 1
        # 解析 else 分支代码块
        else_block_ast = _parse_block(parser_state)
        children.append(else_block_ast)
    
    # 7. 构建 IF_STMT AST 节点
    if_stmt_ast = {
        "type": "IF_STMT",
        "children": children,
        "value": None,
        "line": line,
        "column": column
    }
    
    return if_stmt_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
