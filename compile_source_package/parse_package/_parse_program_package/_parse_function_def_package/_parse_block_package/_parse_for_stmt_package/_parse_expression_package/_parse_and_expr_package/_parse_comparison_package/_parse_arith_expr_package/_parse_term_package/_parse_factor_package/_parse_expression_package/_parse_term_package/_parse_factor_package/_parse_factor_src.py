# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_primary_package._parse_primary_src import _parse_primary

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (PLUS, MINUS, MULTI, DIV, MOD, LPAREN, RPAREN, IDENTIFIER, LITERAL, etc.)
#   "value": str,            # token 值 (+, -, *, /, %, (, ), 标识符名，字面量值等)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, ERROR, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值（运算符字符串或标识符/字面量值）
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
def _parse_factor(parser_state: ParserState) -> AST:
    """解析 factor 层级（括号、一元运算符、primary）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否已到达 token 末尾
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input while parsing factor"
        return {"type": "ERROR", "value": "Unexpected end of input", "children": [], "line": -1, "column": -1}
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    # 情况 1: LPAREN - 解析括号内的表达式
    if token_type == "LPAREN":
        parser_state["pos"] = pos + 1  # 消耗左括号
        expr_ast = _parse_expression(parser_state)
        
        if parser_state.get("error"):
            return expr_ast
        
        # 期望 RPAREN
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens) or tokens[new_pos]["type"] != "RPAREN":
            parser_state["error"] = f"Expected ')' but found {tokens[new_pos]['value'] if new_pos < len(tokens) else 'EOF'}"
            return {"type": "ERROR", "value": "Missing closing parenthesis", "children": [], "line": current_token["line"], "column": current_token["column"]}
        
        parser_state["pos"] = new_pos + 1  # 消耗右括号
        return expr_ast
    
    # 情况 2: PLUS/MINUS - 解析一元运算符
    elif token_type in ("PLUS", "MINUS"):
        op_token = current_token
        parser_state["pos"] = pos + 1  # 消耗一元运算符
        operand_ast = _parse_factor(parser_state)  # 递归解析 factor（右结合）
        
        if parser_state.get("error"):
            return operand_ast
        
        return {
            "type": "UNARY_OP",
            "value": op_token["value"],
            "children": [operand_ast],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    # 情况 3: 解析 primary（IDENTIFIER 或 LITERAL）
    else:
        return _parse_primary(parser_state)

# === helper functions ===

# === OOP compatibility layer ===
