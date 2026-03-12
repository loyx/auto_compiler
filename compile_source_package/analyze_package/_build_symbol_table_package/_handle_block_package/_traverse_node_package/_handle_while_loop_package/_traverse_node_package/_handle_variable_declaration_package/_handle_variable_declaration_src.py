# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# 从父包导入调度函数，用于递归遍历子节点
# Import _traverse_node lazily to avoid circular import
# It will be imported inside the function when needed

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "name": str,             # 变量名
#   "data_type": str,        # 数据类型 ("int" 或 "char")
#   "value": AST,            # 初始值
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list
# }

# === main function ===
def _handle_variable_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 variable_declaration 节点。
    
    输入：
      - node: AST 节点，包含 name、data_type、value 字段
      - symbol_table: 符号表
    
    处理：
      1. 从 node 提取变量名、数据类型、初始值
      2. 在 symbol_table['variables'] 中注册变量信息
      3. 如果存在初始值 (value 字段)，调用 _traverse_node 递归处理
    
    副作用：修改 symbol_table['variables']
    """
    var_name = node.get("name")
    data_type = node.get("data_type")
    value = node.get("value")
    line = node.get("line")
    column = node.get("column")
    
    # 注册变量到符号表
    if var_name and data_type:
        symbol_table["variables"][var_name] = {
            "data_type": data_type,
            "is_declared": True,
            "line": line,
            "column": column,
            "scope_level": symbol_table.get("current_scope", 0)
        }
    
    # 如果有初始值，递归遍历
    if value is not None:
        # Import _traverse_node lazily to avoid circular import
        from .._traverse_node_src import _traverse_node
        _traverse_node(value, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this handler function