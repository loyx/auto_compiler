# === std / third-party imports ===
from typing import Dict, Any

# === sub function imports ===
# only import child functions
from ..expression_package._parse_expression_src import _parse_expression

# === ADT defines ===
# define the data structures used between parent and child functions
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
def _parse_expression_statement(parser_state: ParserState) -> AST:
    """
    解析表达式语句（expression SEMICOLON）。
    
    输入：parser_state，其中 pos 指向表达式起始 token。
    输出：EXPRESSION_STMT AST 节点。
    
    处理逻辑：
    1. 记录起始位置（用于 AST 的 line/column）
    2. 调用 _parse_expression 解析表达式
    3. 消费结束分号
    4. 返回 EXPRESSION_STMT 节点
    
    错误处理：
    - 无法解析表达式：_parse_expression 会抛 SyntaxError
    - 缺少分号：抛 SyntaxError("Expected ';' after expression at line ...")
    """
    # 记录起始位置
    start_pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    
    # 检查是否还有 token
    if start_pos >= len(tokens):
        raise SyntaxError("Unexpected end of file, expected expression")
    
    start_token = tokens[start_pos]
    line = start_token["line"]
    column = start_token["column"]
    
    # 调用表达式解析器
    expression_ast = _parse_expression(parser_state)
    
    # 消费结束分号
    current_pos = parser_state["pos"]
    if current_pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of file, expected ';' at line {line}")
    
    current_token = tokens[current_pos]
    if current_token["type"] != "SEMICOLON":
        raise SyntaxError(f"Expected ';' after expression at line {line}")
    
    # 消费分号 token
    parser_state["pos"] += 1
    
    # 构建 EXPRESSION_STMT AST 节点
    return {
        "type": "EXPRESSION_STMT",
        "line": line,
        "column": column,
        "children": [expression_ast]
    }

# === helper functions ===
# 无 helper 函数，token 操作直接内联实现

# === OOP compatibility layer ===
# 不需要 OOP wrapper，省略