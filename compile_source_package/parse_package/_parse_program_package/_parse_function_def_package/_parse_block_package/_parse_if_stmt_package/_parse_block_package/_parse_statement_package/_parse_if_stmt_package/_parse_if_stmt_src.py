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
def _parse_if_stmt(parser_state: dict) -> dict:
    """
    解析 if 条件语句。
    支持语法：if (cond) { ... } 或 if (cond) { ... } else { ... }
    输入：parser_state（pos 指向 IF 关键字）
    输出：IF_STMT AST 节点
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 记录 IF 关键字的位置
    if_token = tokens[pos]
    line = if_token["line"]
    column = if_token["column"]
    
    # 消费 IF 关键字
    _expect_token(parser_state, "IF")
    
    # 消费 LPAREN
    _expect_token(parser_state, "LPAREN")
    
    # 解析条件表达式
    condition = _parse_expression(parser_state)
    
    # 消费 RPAREN
    _expect_token(parser_state, "RPAREN")
    
    # 解析 then 块
    then_branch = _parse_block(parser_state)
    
    # 检查是否有 else 分支
    else_branch = None
    current_pos = parser_state["pos"]
    if current_pos < len(tokens):
        next_token = tokens[current_pos]
        if next_token["type"] == "ELSE":
            # 消费 ELSE 关键字
            _expect_token(parser_state, "ELSE")
            # 解析 else 块
            else_branch = _parse_block(parser_state)
    
    # 构建 IF_STMT AST 节点
    return {
        "type": "IF_STMT",
        "condition": condition,
        "then_branch": then_branch,
        "else_branch": else_branch,
        "line": line,
        "column": column
    }

# === helper functions ===
def _expect_token(parser_state: dict, expected_type: str) -> None:
    """
    验证并消费期望类型的 token。
    如果当前 token 类型不匹配，抛出 SyntaxError。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(
            f"{parser_state['filename']}:0:0: "
            f"Unexpected end of input, expected '{expected_type}'"
        )
    
    token = tokens[pos]
    if token["type"] != expected_type:
        raise SyntaxError(
            f"{parser_state['filename']}:{token['line']}:{token['column']}: "
            f"Expected '{expected_type}', got '{token['type']}'"
        )
    
    parser_state["pos"] += 1

# === OOP compatibility layer ===
