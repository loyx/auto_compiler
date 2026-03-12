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
#   "name": str,             # 函数名 (function_call 节点使用)
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
#   "scope_stack": list,           # 作用域栈 (存储旧 scope 值)
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (保证已初始化为 [])
# }

# === main function ===
def _handle_function_call(node: AST, symbol_table: SymbolTable) -> None:
    """Handle function_call AST node for semantic analysis."""
    func_name = node.get("name", "")
    line = node.get("line", 0)
    column = node.get("column", 0)
    args = node.get("children", [])

    # Check if function is declared
    functions = symbol_table.get("functions", {})
    if func_name not in functions:
        symbol_table["errors"].append({
            "type": "error",
            "message": f"Function '{func_name}' not declared",
            "line": line,
            "column": column
        })
        return

    func_def = functions[func_name]
    expected_params = func_def.get("params", [])
    expected_count = len(expected_params)
    actual_count = len(args)

    # Validate argument count
    if actual_count != expected_count:
        symbol_table["errors"].append({
            "type": "error",
            "message": f"Function '{func_name}' expects {expected_count} arguments but got {actual_count}",
            "line": line,
            "column": column
        })
        return

    # Validate each argument type
    for i, arg in enumerate(args):
        # Traverse argument expression first
        _traverse_node(arg, symbol_table)

        # Check type match
        param_def = expected_params[i]
        expected_type = param_def.get("type", "")
        actual_type = arg.get("data_type", "")

        if actual_type != expected_type:
            symbol_table["errors"].append({
                "type": "error",
                "message": f"Argument {i} of function '{func_name}' expects type '{expected_type}' but got '{actual_type}'",
                "line": line,
                "column": column
            })

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this semantic analysis function
