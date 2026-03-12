# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_package._parse_multiplicative_src import _parse_multiplicative

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
def _parse_additive(parser_state: ParserState) -> AST:
    """
    解析加法表达式（+、-）。
    语法：multiplicative_expr (add_op multiplicative_expr)*
    左结合构建 AST。
    """
    # 1. 解析左侧操作数
    left = _parse_multiplicative(parser_state)
    
    # 2. 循环处理加法运算符
    while parser_state["pos"] < len(parser_state["tokens"]):
        current_token = parser_state["tokens"][parser_state["pos"]]
        
        # 3. 检查是否为加法运算符
        if current_token["type"] not in ("ADD", "SUB"):
            break
        
        # 4. 记录运算符并消费 token
        op_string = "+" if current_token["type"] == "ADD" else "-"
        op_line = current_token["line"]
        op_column = current_token["column"]
        parser_state["pos"] += 1
        
        # 5. 解析右侧操作数
        right = _parse_multiplicative(parser_state)
        
        # 6. 构建 BINARY_OP 节点（左结合）
        left = {
            "type": "BINARY_OP",
            "value": op_string,
            "children": [left, right],
            "line": left.get("line", op_line),
            "column": left.get("column", op_column)
        }
    
    # 7. 返回最终的 AST 节点
    return left

# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node