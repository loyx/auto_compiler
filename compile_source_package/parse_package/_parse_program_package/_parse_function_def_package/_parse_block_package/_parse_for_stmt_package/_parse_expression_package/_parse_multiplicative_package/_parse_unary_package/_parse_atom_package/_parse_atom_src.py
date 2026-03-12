# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._handle_atom_token_package._handle_atom_token_src import _handle_atom_token

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
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, etc.)
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
def _parse_atom(parser_state: ParserState) -> AST:
    """
    解析原子表达式（atom expression）。
    
    原子表达式类型：IDENTIFIER, LITERAL (NUMBER/INTEGER/STRING/TRUE/FALSE/NONE/NULL), PAREN。
    输入：parser_state，当前位置指向原子表达式起始 token。
    输出：AST 节点（IDENTIFIER/LITERAL 或括号内的表达式）。
    更新 parser_state['pos'] 消费已解析的 token。
    遇到错误时设置 parser_state['error'] 并返回 ERROR 节点。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 检查 EOF
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return {"type": "ERROR", "value": "unexpected_eof", "children": [], "line": 0, "column": 0}
    
    token = tokens[pos]
    token_type = token.get("type", "")
    
    # LPAREN - 括号表达式（特殊处理，需要递归）
    if token_type == "LPAREN":
        parser_state["pos"] = pos + 1  # 消费 LPAREN
        
        # 递归解析括号内表达式
        inner_expr = _parse_expression(parser_state)
        
        # 检查是否有错误
        if parser_state.get("error"):
            return inner_expr
        
        # 匹配并消费 RPAREN
        return _consume_rparen(parser_state, inner_expr)
    
    # 其他原子类型 - 委托给 helper 处理
    return _handle_atom_token(token, parser_state)

# === helper functions ===
def _consume_rparen(parser_state: ParserState, inner_expr: AST) -> AST:
    """匹配并消费 RPAREN token。"""
    tokens = parser_state.get("tokens", [])
    new_pos = parser_state.get("pos", 0)
    
    if new_pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input, expected ')'"
        return {"type": "ERROR", "value": "missing_rparen", "children": [], "line": 0, "column": 0}
    
    rparen_token = tokens[new_pos]
    if rparen_token.get("type") != "RPAREN":
        parser_state["error"] = f"Expected ')', got {rparen_token.get('type')}"
        return {"type": "ERROR", "value": "missing_rparen", "children": [], "line": 0, "column": 0}
    
    parser_state["pos"] = new_pos + 1  # 消费 RPAREN
    return inner_expr

# === OOP compatibility layer ===
# Not needed for this parser function