# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block" 等)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }

# === main function ===
def _handle_return_statement(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 return 语句节点，递归处理返回值表达式。
    
    处理逻辑：
    1. 遍历 node["children"] 查找返回值表达式子节点
    2. 如果存在返回值表达式，调用 _traverse_node 处理
    3. 如果没有返回值（void return），静默跳过
    4. 不需要特殊的作用域管理
    """
    if "children" not in node:
        return
    
    for child in node["children"]:
        if isinstance(child, dict) and child.get("type") == "expression":
            _traverse_node(child, symbol_table)

# === helper functions ===

# === OOP compatibility layer ===
