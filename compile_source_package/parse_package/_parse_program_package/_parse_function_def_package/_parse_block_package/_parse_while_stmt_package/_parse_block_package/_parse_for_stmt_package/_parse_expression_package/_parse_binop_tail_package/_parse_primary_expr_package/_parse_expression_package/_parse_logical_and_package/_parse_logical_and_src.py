# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_equality_package._parse_equality_src import _parse_equality

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,          # token 类型，如 "AND", "EQUAL", "IDENT", etc.
#   "value": str,         # token 原始值
#   "line": int,          # 行号
#   "column": int         # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,          # 节点类型，如 "BINARY_OP", "IDENT", "ERROR"
#   "children": list,     # 子节点列表
#   "value": Any,         # 节点值
#   "operator": str,      # 运算符，如 "&&", "==", "!="
#   "line": int,          # 行号
#   "column": int         # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,       # Token 列表
#   "pos": int,           # 当前位置索引
#   "filename": str,      # 源文件名
#   "error": str          # 错误信息（可选）
# }

# === main function ===
def _parse_logical_and(parser_state: ParserState) -> AST:
    """
    解析逻辑与表达式 (&&)。
    处理左结合的 && 运算符，调用 _parse_equality 获取操作数。
    """
    # 获取左侧操作数
    left = _parse_equality(parser_state)
    
    # 检查是否有错误
    if left.get("type") == "ERROR":
        return left
    
    # 循环处理左结合的 && 运算符
    while True:
        # 检查当前位置是否超出范围
        if parser_state["pos"] >= len(parser_state["tokens"]):
            break
        
        current_token = parser_state["tokens"][parser_state["pos"]]
        
        # 检查是否为 AND (&&) 运算符
        if current_token.get("type") != "AND":
            break
        
        # 记录运算符位置
        op_line = current_token.get("line", 0)
        op_column = current_token.get("column", 0)
        
        # 递增 pos，跳过 && 运算符
        parser_state["pos"] += 1
        
        # 获取右侧操作数
        right = _parse_equality(parser_state)
        
        # 检查右侧操作数是否有错误
        if right.get("type") == "ERROR":
            parser_state["error"] = f"Missing operand after && at line {op_line}, column {op_column}"
            return right
        
        # 构建 BINARY_OP 节点
        left = {
            "type": "BINARY_OP",
            "operator": "&&",
            "children": [left, right],
            "line": op_line,
            "column": op_column
        }
    
    return left

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node