# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (如变量名、函数名、字面量值等)
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
#   "scope_stack": list,           # 作用域栈 (存储旧 scope 值)
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }

# === main function ===
def _handle_function_call(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理函数调用节点：验证函数已声明，遍历参数表达式。
    
    副作用：可能修改 symbol_table["errors"]
    """
    func_name = node.get("value")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 验证函数是否已声明
    functions = symbol_table.get("functions", {})
    if func_name not in functions:
        errors = symbol_table.setdefault("errors", [])
        errors.append({
            "error_type": "undeclared_function",
            "func_name": func_name,
            "line": line,
            "column": column
        })
        return
    
    # 遍历参数表达式
    children = node.get("children", [])
    for param_node in children:
        _traverse_node(param_node, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node