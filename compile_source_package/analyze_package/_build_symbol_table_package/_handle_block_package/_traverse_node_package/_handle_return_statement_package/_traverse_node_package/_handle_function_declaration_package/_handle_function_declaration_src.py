# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# _traverse_node will be imported at runtime to avoid circular/missing import issues
# For testing purposes, this can be patched
_traverse_node = None

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "function_declaration")
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "name": str,             # 函数名
#   "return_type": str,      # 返回类型 ("int" 或 "char")
#   "params": list           # 参数列表
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
def _handle_function_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle function_declaration type AST nodes.
    Extract function info and register to symbol_table, detecting duplicate declarations.
    """
    # Initialize functions dict if not exists
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    
    # Extract function name
    func_name = node.get("value")
    if not func_name:
        for child in node.get("children", []):
            if child.get("type") == "identifier":
                func_name = child.get("value")
                break
    
    # Extract line and column
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # Extract return type
    return_type = node.get("data_type", "int")
    
    # Extract parameters from children
    params = []
    for child in node.get("children", []):
        if child.get("type") == "parameter":
            params.append({
                "name": child.get("value"),
                "data_type": child.get("data_type", "int")
            })
    
    # Check for duplicate declaration
    if func_name in symbol_table["functions"]:
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append(
            f"Error: Function '{func_name}' already declared at line {line}, column {column}"
        )
    else:
        # Register function
        symbol_table["functions"][func_name] = {
            "return_type": return_type,
            "params": params,
            "line": line,
            "column": column
        }
    
    # Set current function
    symbol_table["current_function"] = func_name
    
    # Manually traverse children for function body (block nodes)
    # Import locally to avoid circular/missing import issues
    # If _traverse_node is None (or patched), use the global reference
    global _traverse_node
    if _traverse_node is None:
        from ._traverse_node_package._traverse_node_src import _traverse_node as _tn
        _traverse_node = _tn
    for child in node.get("children", []):
        if child.get("type") == "block":
            _traverse_node(child, symbol_table)


# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# Not required for this function node
