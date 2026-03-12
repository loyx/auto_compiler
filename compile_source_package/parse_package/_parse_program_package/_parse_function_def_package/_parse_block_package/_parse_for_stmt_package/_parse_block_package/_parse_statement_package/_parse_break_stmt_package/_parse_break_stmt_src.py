# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions required for this simple parser node

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
#   "type": str,             # 节点类型 (BREAK_STMT, etc.)
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
    
    语法格式：break;
    
    步骤：
    1. 消耗 BREAK token
    2. 消耗分号 token
    3. 返回 BREAK_STMT 类型 AST 节点
    
    输入：parser_state（pos 指向 BREAK token）
    输出：BREAK_STMT 类型 AST 节点
    副作用：原地更新 parser_state["pos"] 到分号之后的位置
    错误：缺少分号时抛出 SyntaxError
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 步骤 1: 消耗 BREAK token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected 'break'")
    
    break_token = tokens[pos]
    if break_token.get("type") != "BREAK":
        raise SyntaxError(f"Expected BREAK token, got {break_token.get('type')}")
    
    break_line = break_token.get("line", 0)
    break_column = break_token.get("column", 0)
    pos += 1
    
    # 步骤 2: 消耗分号 token
    if pos >= len(tokens):
        # 更新 parser_state 位置到当前位置（BREAK 已消耗）
        parser_state["pos"] = pos
        raise SyntaxError("Unexpected end of input, expected ';' after break")
    
    semicolon_token = tokens[pos]
    if semicolon_token.get("type") != "SEMICOLON":
        # 更新 parser_state 位置到当前位置（BREAK 已消耗）
        parser_state["pos"] = pos
        raise SyntaxError(f"Expected ';' after break, got {semicolon_token.get('value')}")
    
    pos += 1
    
    # 更新 parser_state 位置
    parser_state["pos"] = pos
    
    # 步骤 3: 返回 BREAK_STMT 类型 AST 节点
    ast_node: AST = {
        "type": "BREAK_STMT",
        "children": [],
        "value": None,
        "line": break_line,
        "column": break_column
    }
    
    return ast_node

# === helper functions ===
# No helper functions needed for this simple parser node

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function nodes