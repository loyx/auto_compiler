# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._expect_token_package._expect_token_src import _expect_token

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }


# === main function ===
def _parse_expr_or_assign_stmt(parser_state: ParserState) -> AST:
    """
    解析以 IDENTIFIER 开头的语句：表达式语句或赋值语句。
    通过向前看下一个 token 区分：若是 ASSIGN 则为赋值语句，否则为表达式语句。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 解析左侧表达式（至少包含 IDENTIFIER）
    left_expr = _parse_expression(parser_state)
    
    # 向前看下一个 token
    if parser_state["pos"] < len(tokens):
        next_token = tokens[parser_state["pos"]]
    else:
        next_token = None
    
    # 判断是否为赋值语句
    if next_token and next_token["type"] == "ASSIGN":
        # 消耗 ASSIGN token
        _expect_token(parser_state, "ASSIGN")
        
        # 解析右侧表达式
        right_expr = _parse_expression(parser_state)
        
        # 构建 ASSIGN_STMT AST 节点
        assign_stmt = {
            "type": "ASSIGN_STMT",
            "children": [left_expr, right_expr],
            "value": "=",
            "line": left_expr.get("line", 0),
            "column": left_expr.get("column", 0)
        }
        
        # 消耗 SEMICOLON
        _expect_token(parser_state, "SEMICOLON")
        
        return assign_stmt
    else:
        # 表达式语句：消耗 SEMICOLON
        _expect_token(parser_state, "SEMICOLON")
        
        # 构建 EXPR_STMT AST 节点
        expr_stmt = {
            "type": "EXPR_STMT",
            "children": [left_expr],
            "value": None,
            "line": left_expr.get("line", 0),
            "column": left_expr.get("column", 0)
        }
        
        return expr_stmt


# === helper functions ===


# === OOP compatibility layer ===
