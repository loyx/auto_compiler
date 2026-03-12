# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .. import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
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
#   "errors": list                 # 错误列表 (可选)
# }


# === main function ===
def _handle_return(node: AST, symbol_table: SymbolTable) -> None:
    """Process return statement node and validate return type matches function declaration."""
    # Ensure errors list exists
    if "errors" not in symbol_table:
        symbol_table["errors"] = []

    # Get current function name
    current_function = symbol_table.get("current_function")

    # Check if return is used outside of function
    if not current_function:
        error_entry = {
            "type": "error",
            "message": "return statement outside of function",
            "line": node.get("line", -1),
            "column": node.get("column", -1)
        }
        symbol_table["errors"].append(error_entry)
        return

    # Get expected return type from function declaration
    functions = symbol_table.get("functions", {})
    func_info = functions.get(current_function, {})
    expected_type = func_info.get("return_type")

    # Get return value expression (if any)
    children = node.get("children", [])

    if len(children) == 0:
        # Void return (no expression)
        if expected_type and expected_type != "void":
            error_entry = {
                "type": "error",
                "message": f"Return type mismatch: expected {expected_type}, got void",
                "line": node.get("line", -1),
                "column": node.get("column", -1)
            }
            symbol_table["errors"].append(error_entry)
    else:
        # Return with expression - traverse the expression first
        return_expr = children[0]
        _traverse_node(return_expr, symbol_table)

        # Get actual type from the expression node's data_type field
        actual_type = return_expr.get("data_type")

        # Compare types
        if expected_type and actual_type and expected_type != actual_type:
            error_entry = {
                "type": "error",
                "message": f"Return type mismatch: expected {expected_type}, got {actual_type}",
                "line": node.get("line", -1),
                "column": node.get("column", -1)
            }
            symbol_table["errors"].append(error_entry)


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
