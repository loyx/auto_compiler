# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Import _traverse_node from parent module for recursive AST traversal
# Using deferred import to avoid circular dependency

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "name": str,             # 函数名
#   "params": list,          # 参数列表
#   "body": AST,             # 函数体
#   "return_type": str,      # 返回类型
#   "line": int,
#   "column": int,
#   "target": str,           # 赋值目标变量名 (assignment 节点特有)
#   "value": AST             # 赋值表达式 (assignment 节点特有)
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {type, line, column, ...}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,
#   "scope_stack": list
# }

# === main function ===
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理赋值语句节点。
    
    输入：assignment 类型的 AST 节点和符号表。
    处理：检查目标变量是否已声明，验证赋值类型兼容性，递归处理赋值表达式。
    副作用：可能修改 symbol_table['variables']。
    """
    # Step 1: Extract target variable name from node
    target = node.get("target")
    
    # Step 2: Extract value expression from node
    value = node.get("value")
    
    # Step 3: Check if target variable exists in symbol_table
    variables = symbol_table.get("variables", {})
    if target not in variables:
        # Variable not previously declared - this may be a new declaration
        # Record the variable with basic info from the assignment node
        variables[target] = {
            "line": node.get("line"),
            "column": node.get("column"),
            "scope": symbol_table.get("current_scope", 0)
        }
    
    # Step 4: Recursively traverse the value expression
    if value is not None:
        # Deferred import to avoid circular dependency
        from .._traverse_node_src import _traverse_node
        _traverse_node(value, symbol_table)
    
    # Step 5: (Optional) Update variable info with value type if inferable
    # This can be extended based on type inference requirements

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# Not required - this is a helper function node, not a framework entry point
