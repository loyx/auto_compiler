# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No sub functions delegated for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "return_statement")
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
    Handle return_statement type AST node.
    
    Validates:
    1. Return statement is inside a function
    2. Return type matches function declaration
    3. Recursively processes return value expression
    """
    # Get current function name
    current_function: Optional[str] = symbol_table.get("current_function")
    
    # Get line number for error reporting
    line: int = node.get("line", 0)
    
    # Check if we're inside a function
    if current_function is None:
        error_msg: str = f"return statement outside function at line {line}"
        errors_list: list = symbol_table.get("errors", [])
        errors_list.append(error_msg)
        symbol_table["errors"] = errors_list
        return
    
    # Get function declaration from symbol table
    functions_dict: Dict[str, Any] = symbol_table.get("functions", {})
    func_info: Optional[Dict] = functions_dict.get(current_function)
    
    if func_info is None:
        error_msg: str = f"function '{current_function}' not found in symbol table at line {line}"
        errors_list = symbol_table.get("errors", [])
        errors_list.append(error_msg)
        symbol_table["errors"] = errors_list
        return
    
    # Get expected return type
    expected_return_type: str = func_info.get("return_type", "void")
    
    # Get return value from node
    children: list = node.get("children", [])
    node_value: Any = node.get("value")
    
    # Determine actual return type first
    actual_return_type: Optional[str] = None
    
    # Try to get type from node's data_type field
    if node.get("data_type"):
        actual_return_type = node.get("data_type")
    # Try to get type from first child (expression)
    elif len(children) > 0 and isinstance(children[0], dict):
        first_child: Dict = children[0]
        actual_return_type = first_child.get("data_type")
    
    # Check if return has a value (based on whether we have type info or children/value)
    has_return_value: bool = actual_return_type is not None or len(children) > 0 or node_value is not None
    
    if has_return_value:
        # If we have type information, validate it
        if actual_return_type is not None:
            if actual_return_type != expected_return_type:
                error_msg = f"Return type mismatch: expected {expected_return_type} but got {actual_return_type} at line {line}"
                errors_list = symbol_table.get("errors", [])
                errors_list.append(error_msg)
                symbol_table["errors"] = errors_list
        
        # Recursively process children nodes
        for child in children:
            if isinstance(child, dict):
                _traverse_node(child, symbol_table)
    else:
        # Void return - check if function expects void
        if expected_return_type not in ["void", None, ""]:
            error_msg = f"Function '{current_function}' expects return type {expected_return_type} but got void at line {line}"
            errors_list = symbol_table.get("errors", [])
            errors_list.append(error_msg)
            symbol_table["errors"] = errors_list


# === helper functions ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    Recursively traverse AST nodes.
    
    This is a helper function to process child nodes of return statements.
    It dispatches to appropriate handlers based on node type.
    """
    if not isinstance(node, dict):
        return
    
    node_type: str = node.get("type", "")
    
    # Dispatch based on node type
    if node_type == "return_statement":
        _handle_return_statement(node, symbol_table)
    # Add other node type handlers as needed
    # For now, we just traverse children for unknown types
    else:
        children: list = node.get("children", [])
        for child in children:
            if isinstance(child, dict):
                _traverse_node(child, symbol_table)


# === OOP compatibility layer ===
# No OOP wrapper needed - this is a helper function node