# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Note: _traverse_node is imported inside the function to avoid circular import

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
#   "errors": list                 # 错误列表
# }

# === main function ===
def _handle_function_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle function_declaration AST node: register function declaration,
    manage scope, process parameters, and traverse function body.
    """
    # 1. Extract function name from identifier child node
    func_name = None
    for child in node.get("children", []):
        if child.get("type") == "identifier":
            func_name = child.get("value")
            break
    
    if func_name is None:
        return  # Cannot process without function name
    
    # 2. Extract return type from node["data_type"]
    return_type = node.get("data_type", "int")
    
    # 3. Check for duplicate declaration
    if func_name in symbol_table["functions"]:
        symbol_table["errors"].append({
            "type": "duplicate_function",
            "message": f"Function '{func_name}' already declared",
            "line": node.get("line"),
            "column": node.get("column")
        })
        return  # Stop processing on duplicate
    
    # 4. Extract parameters from parameter child nodes
    params = []
    for child in node.get("children", []):
        if child.get("type") == "parameter":
            params.append({
                "name": child.get("value"),
                "data_type": child.get("data_type", "int")
            })
    
    # 5. Register function to symbol_table
    symbol_table["functions"][func_name] = {
        "return_type": return_type,
        "params": params,
        "line": node.get("line"),
        "column": node.get("column")
    }
    
    # 6. Set current_function and enter function scope
    previous_function = symbol_table.get("current_function")
    symbol_table["current_function"] = func_name
    symbol_table["current_scope"] += 1
    symbol_table["scope_stack"].append(func_name)
    
    # 7. Add parameters to variables
    scope_level = symbol_table["current_scope"]
    for param in params:
        param_name = param["name"]
        symbol_table["variables"][param_name] = {
            "data_type": param["data_type"],
            "is_declared": True,
            "line": node.get("line"),
            "column": node.get("column"),
            "scope_level": scope_level
        }
    
    # 8. Traverse function body (all child nodes)
    # Import here to avoid circular import
    from ._traverse_node_package._traverse_node_src import _traverse_node
    for child in node.get("children", []):
        _traverse_node(child, symbol_table)
    
    # 9. Exit function scope and restore current_function
    symbol_table["current_scope"] -= 1
    symbol_table["scope_stack"].pop()
    symbol_table["current_function"] = previous_function

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
