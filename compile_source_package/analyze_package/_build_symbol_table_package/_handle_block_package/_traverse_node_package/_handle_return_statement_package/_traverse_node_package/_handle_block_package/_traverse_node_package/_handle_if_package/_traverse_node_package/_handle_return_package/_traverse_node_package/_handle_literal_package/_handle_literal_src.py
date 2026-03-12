# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple literal handler

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("literal_int" / "int_literal" / "literal_char" / "char_literal")
#   "value": Any,            # 字面量的值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_literal(node: AST, symbol_table: SymbolTable) -> str:
    """
    处理字面量节点并返回其类型。
    
    处理逻辑：
    1. 检查 node["type"]
    2. 如果是 "literal_int" 或 "int_literal"，返回 "int"
    3. 如果是 "literal_char" 或 "char_literal"，返回 "char"
    4. 其他情况返回 "void"
    
    副作用：无
    返回：类型字符串 ("int" 或 "char" 或 "void")
    """
    node_type = node.get("type", "")
    
    if node_type in ("literal_int", "int_literal"):
        return "int"
    elif node_type in ("literal_char", "char_literal"):
        return "char"
    else:
        return "void"

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
