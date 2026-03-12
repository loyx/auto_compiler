# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_package._parse_comparison_src import _parse_comparison

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
#   "operator": str,
#   "line": int,
#   "column": int
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_logical_and(parser_state: ParserState) -> AST:
    """
    解析逻辑与表达式 (&&)。
    优先级：高于 ||，低于比较运算符。
    结合性：左结合。
    """
    # 获取左侧操作数（调用更低优先级的解析函数）
    left = _parse_comparison(parser_state)
    
    # 检查是否有错误
    if parser_state.get("error"):
        return left
    
    # 循环处理左结合的 && 运算符
    while _is_current_token_and(parser_state):
        # 记录运算符位置
        op_token = _get_current_token(parser_state)
        op_line = op_token.get("line", 0)
        op_column = op_token.get("column", 0)
        
        # 递增 pos，消耗 && token
        parser_state["pos"] += 1
        
        # 解析右侧操作数
        right = _parse_comparison(parser_state)
        
        # 检查错误：&& 后缺少操作数
        if parser_state.get("error"):
            return _create_error_node(parser_state, "Missing operand after &&")
        
        # 构建 BINARY_OP 节点（左结合）
        left = {
            "type": "BINARY_OP",
            "operator": "&&",
            "children": [left, right],
            "line": op_line,
            "column": op_column
        }
    
    return left

# === helper functions ===
def _is_current_token_and(parser_state: ParserState) -> bool:
    """检查当前 token 是否为 AND (&&) 运算符。"""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    
    if pos >= len(tokens):
        return False
    
    token = tokens[pos]
    return token.get("type") == "AND"

def _get_current_token(parser_state: ParserState) -> Token:
    """获取当前 token。"""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    
    if pos >= len(tokens):
        return {"type": "EOF", "value": "", "line": 0, "column": 0}
    
    return tokens[pos]

def _create_error_node(parser_state: ParserState, message: str) -> AST:
    """创建错误 AST 节点。"""
    parser_state["error"] = message
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    
    line = 0
    column = 0
    if pos < len(tokens):
        token = tokens[pos]
        line = token.get("line", 0)
        column = token.get("column", 0)
    
    return {
        "type": "ERROR",
        "value": message,
        "children": [],
        "line": line,
        "column": column
    }

# === OOP compatibility layer ===
# Not required for parser function nodes