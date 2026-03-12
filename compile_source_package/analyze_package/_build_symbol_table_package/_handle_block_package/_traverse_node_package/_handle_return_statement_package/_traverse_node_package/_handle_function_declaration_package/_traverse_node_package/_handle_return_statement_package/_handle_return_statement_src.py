# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_return_statement(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle return_statement nodes by validating return type matches function signature.
    
    Modifies symbol_table in-place by appending error messages to symbol_table["errors"].
    Returns None.
    """
    # Extract return value's data_type from node
    return_type = node.get("data_type")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # Get current function name from symbol_table
    current_function = symbol_table.get("current_function")
    
    # Case: Return statement outside function context
    if current_function is None:
        error_msg = f"Error: Return statement outside function at line {line}, column {column}"
        errors_list = symbol_table.get("errors", [])
        if isinstance(errors_list, list):
            errors_list.append(error_msg)
        return
    
    # Look up current function in symbol_table["functions"]
    if "functions" not in symbol_table:
        return
    
    functions_dict = symbol_table.get("functions", {})
    if not isinstance(functions_dict, dict):
        return
    
    func_info = functions_dict.get(current_function)
    if func_info is None:
        error_msg = f"Error: Return statement outside function at line {line}, column {column}"
        errors_list = symbol_table.get("errors", [])
        if isinstance(errors_list, list):
            errors_list.append(error_msg)
        return
    
    # Get expected return type from function signature
    expected_type = func_info.get("return_type")
    
    # Compare node's data_type with function's declared return_type
    if return_type is not None and expected_type is not None:
        if return_type != expected_type:
            error_msg = f"Error: Return type '{return_type}' does not match function '{current_function}' return type '{expected_type}' at line {line}, column {column}"
            errors_list = symbol_table.get("errors", [])
            if isinstance(errors_list, list):
                errors_list.append(error_msg)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
