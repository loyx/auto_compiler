# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple parser node

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
#   "type": str,             # 节点类型 (PROGRAM, FUNCTION_DEF, PARAM, VAR_DECL, IF_STMT, WHILE_STMT, FOR_STMT, RETURN_STMT, BREAK_STMT, CONTINUE_STMT, EXPR_STMT, BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, BLOCK)
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
def _parse_break_stmt(parser_state: ParserState) -> AST:
    """
    解析 break 语句。
    
    输入：parser_state（当前位置指向 BREAK token）
    输出：BREAK_STMT 类型 AST 节点
    错误：遇到语法错误时抛出 SyntaxError
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 验证当前位置确实是 BREAK token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected 'break' statement")
    
    current_token = tokens[pos]
    if current_token.get("type") != "BREAK":
        raise SyntaxError(f"Expected BREAK token, got {current_token.get('type')} at line {current_token.get('line')}")
    
    # 记录 break 语句的位置信息
    line = current_token.get("line")
    column = current_token.get("column")
    
    # 消费 BREAK token
    parser_state["pos"] = pos + 1
    
    # 消费分号（如果有）
    new_pos = parser_state["pos"]
    if new_pos < len(tokens):
        next_token = tokens[new_pos]
        if next_token.get("type") == "SEMICOLON":
            parser_state["pos"] = new_pos + 1
    
    # 构建并返回 BREAK_STMT AST 节点
    return {
        "type": "BREAK_STMT",
        "children": [],
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed for this simple parser node

# === OOP compatibility layer ===
# Not needed for parser function nodes