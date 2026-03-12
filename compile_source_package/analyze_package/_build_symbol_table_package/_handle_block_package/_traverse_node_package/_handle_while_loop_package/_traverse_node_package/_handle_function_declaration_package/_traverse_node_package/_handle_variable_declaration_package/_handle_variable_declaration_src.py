# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "name": str,
#   "var_type": str,
#   "initial_value": AST,
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list
# }


# === main function ===
def _handle_variable_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量声明节点，将变量信息注册到符号表中。
    
    处理逻辑：
    1. 从 node 中提取变量名、类型、位置信息
    2. 将变量注册到 symbol_table["variables"]
    3. 如果存在 initial_value，递归调用 _traverse_node 处理表达式
    """
    name = node.get("name")
    var_type = node.get("var_type")
    line = node.get("line")
    column = node.get("column")
    initial_value = node.get("initial_value")
    
    # 初始化 variables 字典（如果不存在）
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # 注册变量到符号表
    symbol_table["variables"][name] = {
        "type": var_type,
        "line": line,
        "column": column,
        "initial_value": initial_value
    }
    
    # 递归遍历初始化表达式
    if initial_value is not None:
        _traverse_node(initial_value, symbol_table)


# === helper functions ===
# No helper functions needed for this simple handler

# === OOP compatibility layer ===
# No OOP wrapper needed for handler function