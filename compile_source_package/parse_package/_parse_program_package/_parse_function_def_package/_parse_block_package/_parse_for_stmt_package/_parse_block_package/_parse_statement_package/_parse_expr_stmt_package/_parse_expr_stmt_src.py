# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression

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
#   "type": str,             # 节点类型 (PROGRAM, FUNCTION_DEF, PARAM, VAR_DECL, IF_STMT, WHILE_STMT, FOR_STMT, RETURN_STMT, BREAK_STMT, CONTINUE_STMT, EXPR_STMT, BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, BLOCK, CALL, INDEX, ACCESS)
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
def _parse_expr_stmt(parser_state: ParserState) -> AST:
    """
    解析表达式语句。
    语法格式：expression;
    输入：parser_state（pos 指向表达式起始 token）
    输出：EXPR_STMT 类型 AST 节点
    副作用：原地更新 parser_state["pos"] 到分号之后的位置
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否还有 token
    if pos >= len(tokens):
        filename = parser_state.get("filename", "unknown")
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input while parsing expression statement")
    
    # 记录起始位置
    start_line = tokens[pos]["line"]
    start_column = tokens[pos]["column"]
    
    # 调用表达式解析函数
    expr_ast = _parse_expression(parser_state)
    
    # 消耗分号
    current_pos = parser_state["pos"]
    if current_pos >= len(tokens):
        filename = parser_state.get("filename", "unknown")
        raise SyntaxError(f"{filename}:{start_line}:{start_column}: Expected ';' after expression")
    
    if tokens[current_pos]["type"] != "SEMICOLON":
        filename = parser_state.get("filename", "unknown")
        token_type = tokens[current_pos]["type"]
        raise SyntaxError(f"{filename}:{start_line}:{start_column}: Expected ';' after expression, got '{token_type}'")
    
    parser_state["pos"] += 1
    
    # 构建 EXPR_STMT 节点
    return {
        "type": "EXPR_STMT",
        "children": [expr_ast],
        "line": start_line,
        "column": start_column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function