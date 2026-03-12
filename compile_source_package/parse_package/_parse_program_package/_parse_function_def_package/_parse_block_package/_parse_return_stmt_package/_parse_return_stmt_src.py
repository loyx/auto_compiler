# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Module-level reference for _parse_expression, can be mocked in tests
_parse_expression = None

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
def _parse_return_stmt(parser_state: ParserState) -> AST:
    """解析 return 语句，生成 RETURN_STMT 类型 AST 节点。"""
    global _parse_expression
    
    # Lazy import to allow unittest.mock.patch to work correctly
    if _parse_expression is None:
        from ._parse_expression_package._parse_expression_src import _parse_expression as _real_parse_expression
        _parse_expression = _real_parse_expression
    
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 确保当前位置是 RETURN token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected 'return' statement")
    
    current_token = tokens[pos]
    if current_token["type"] != "RETURN":
        raise SyntaxError(f"Expected RETURN token, got {current_token['type']} at line {current_token['line']}, column {current_token['column']}")
    
    # 记录 RETURN token 的位置信息
    line = current_token["line"]
    column = current_token["column"]
    
    # 消费 RETURN token
    pos += 1
    
    # 初始化 RETURN_STMT 节点
    return_node: AST = {
        "type": "RETURN_STMT",
        "children": [],
        "line": line,
        "column": column
    }
    
    # 检查是否有返回值表达式
    if pos < len(tokens):
        next_token = tokens[pos]
        # 如果下一 token 不是分号或右花括号，则解析表达式
        if next_token["type"] not in ("SEMICOLON", "RBRACE"):
            # 解析返回值表达式
            expr_node = _parse_expression(parser_state)
            return_node["children"].append(expr_node)
            # 更新位置（_parse_expression 会修改 parser_state["pos"]）
            pos = parser_state["pos"]
    
    # 消费分号（如果有）
    if pos < len(tokens) and tokens[pos]["type"] == "SEMICOLON":
        pos += 1
        parser_state["pos"] = pos
    
    return return_node

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
