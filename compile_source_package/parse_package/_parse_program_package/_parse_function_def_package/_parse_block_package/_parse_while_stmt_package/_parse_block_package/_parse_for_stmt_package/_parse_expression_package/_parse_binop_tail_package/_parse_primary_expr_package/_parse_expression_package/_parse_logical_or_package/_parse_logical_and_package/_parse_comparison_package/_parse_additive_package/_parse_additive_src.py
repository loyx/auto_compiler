# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_package._parse_multiplicative_src import _parse_multiplicative

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
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_additive(parser_state: ParserState) -> AST:
    """
    解析加法/减法表达式（+，-）。
    优先级高于比较运算符但低于乘除运算符。
    左结合性。
    """
    # 获取左侧操作数（调用更低优先级解析函数）
    left = _parse_multiplicative(parser_state)
    
    # 检查是否已经发生错误
    if parser_state.get("error"):
        return left
    
    tokens = parser_state["tokens"]
    
    # 循环处理连续的加减运算（左结合）
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        # 检查是否为加法或减法运算符
        if current_token["type"] not in ("PLUS", "MINUS"):
            break
        
        # 记录运算符
        operator = current_token["value"]
        op_line = current_token.get("line", 0)
        op_column = current_token.get("column", 0)
        
        # 递增 pos，消耗运算符 token
        parser_state["pos"] += 1
        
        # 获取右侧操作数
        right = _parse_multiplicative(parser_state)
        
        # 检查是否发生错误（运算符后缺少操作数）
        if parser_state.get("error"):
            return {
                "type": "ERROR",
                "value": f"Expected operand after {operator}",
                "line": op_line,
                "column": op_column
            }
        
        # 构建 BINARY_OP 节点
        left = {
            "type": "BINARY_OP",
            "operator": operator,
            "children": [left, right],
            "line": op_line,
            "column": op_column
        }
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node