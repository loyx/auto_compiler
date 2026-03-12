# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_block_package._parse_block_src import _parse_block
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_var_decl_package._parse_var_decl_src import _parse_var_decl

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
def _parse_for_stmt(parser_state: ParserState) -> AST:
    """解析 for 语句，语法：for ( 初始化 ; 条件 ; 更新 ) 语句块
    
    Args:
        parser_state: 解析器状态，pos 指向 FOR token
        
    Returns:
        FOR_STMT AST 节点，children 包含 [init_ast, condition_ast, update_ast, body_ast]
        
    Raises:
        SyntaxError: 语法错误时抛出
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "unknown")
    
    # 1. 检查当前 token 必须是 FOR
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:EOF: 期望 'for' 但遇到文件结束")
    
    current_token = tokens[pos]
    if current_token["type"] != "FOR":
        raise SyntaxError(
            f"{filename}:{current_token['line']}:{current_token['column']}: "
            f"期望 'for' 但遇到 '{current_token['value']}'"
        )
    
    # 记录 for 语句的行列位置
    line = current_token["line"]
    column = current_token["column"]
    
    # 2. 消耗 FOR token
    parser_state["pos"] += 1
    
    # 3. 检查并消耗 LPAREN
    _expect_and_consume(parser_state, "LPAREN", "(")
    
    # 4. 解析初始化部分
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError(f"{filename}:EOF: 期望初始化表达式或变量声明")
    
    # 判断是变量声明还是表达式
    if tokens[parser_state["pos"]]["type"] == "VAR":
        init_ast = _parse_var_decl(parser_state)
    else:
        init_ast = _parse_expression(parser_state)
    
    # 5. 检查并消耗第一个 SEMICOLON
    _expect_and_consume(parser_state, "SEMICOLON", ";")
    
    # 6. 解析条件部分（可为空）
    condition_ast = None
    if parser_state["pos"] < len(tokens) and tokens[parser_state["pos"]]["type"] != "SEMICOLON":
        condition_ast = _parse_expression(parser_state)
    
    # 7. 检查并消耗第二个 SEMICOLON
    _expect_and_consume(parser_state, "SEMICOLON", ";")
    
    # 8. 解析更新部分（可为空）
    update_ast = None
    if parser_state["pos"] < len(tokens) and tokens[parser_state["pos"]]["type"] != "RPAREN":
        update_ast = _parse_expression(parser_state)
    
    # 9. 检查并消耗 RPAREN
    _expect_and_consume(parser_state, "RPAREN", ")")
    
    # 10. 解析循环体语句块
    body_ast = _parse_block(parser_state)
    
    # 11. 返回 FOR_STMT AST 节点
    return {
        "type": "FOR_STMT",
        "children": [init_ast, condition_ast, update_ast, body_ast],
        "line": line,
        "column": column
    }

# === helper functions ===
def _expect_and_consume(parser_state: ParserState, expected_type: str, expected_value: str) -> None:
    """检查并消耗指定类型的 token
    
    Args:
        parser_state: 解析器状态
        expected_type: 期望的 token 类型
        expected_value: 期望的 token 值（用于错误信息）
        
    Raises:
        SyntaxError: 如果当前 token 类型不匹配
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "unknown")
    
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:EOF: 期望 '{expected_value}' 但遇到文件结束")
    
    current_token = tokens[pos]
    if current_token["type"] != expected_type:
        raise SyntaxError(
            f"{filename}:{current_token['line']}:{current_token['column']}: "
            f"期望 '{expected_value}' 但遇到 '{current_token['value']}'"
        )
    
    parser_state["pos"] += 1

# === OOP compatibility layer ===
# 不需要 OOP wrapper