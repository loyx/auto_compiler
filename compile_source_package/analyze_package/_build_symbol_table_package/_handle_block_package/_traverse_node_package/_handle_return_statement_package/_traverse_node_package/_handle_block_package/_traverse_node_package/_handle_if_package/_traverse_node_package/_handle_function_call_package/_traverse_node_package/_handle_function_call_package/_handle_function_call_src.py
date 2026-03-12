# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", "literal", "identifier", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "name": str,             # 名称 (function_call / identifier 节点使用)
#   "value": Any,            # 节点值 (literal 节点使用)
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
    """Handle function_call AST node during semantic analysis."""
    name = node.get("name", "")
    line = node.get("line", 0)
    column = node.get("column", 0)
    children = node.get("children", [])
    
    # Check if function is declared
    functions = symbol_table.get("functions", {})
    if name not in functions:
        error = {
            "type": "error",
            "message": f"Undefined function: {name}",
            "line": line,
            "column": column
        }
        symbol_table["errors"].append(error)
        return
    
    # Function is declared, validate parameter count (optional enhancement)
    func_info = functions[name]
    expected_params = func_info.get("params", [])
    actual_params = len(children)
    
    if len(expected_params) != actual_params:
        error = {
            "type": "error",
            "message": f"Function '{name}' expects {len(expected_params)} arguments, got {actual_params}",
            "line": line,
            "column": column
        }
        symbol_table["errors"].append(error)
    
    # Recursively traverse parameter children
    for param_node in children:
        _traverse_node(param_node, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this semantic analysis function
