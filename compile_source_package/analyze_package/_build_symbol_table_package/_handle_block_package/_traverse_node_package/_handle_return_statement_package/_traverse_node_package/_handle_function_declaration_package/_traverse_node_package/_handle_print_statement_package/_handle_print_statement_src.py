# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this implementation

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
def _handle_print_statement(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle print_statement nodes by validating variable references.
    
    Validates that any variable references in print arguments have been declared.
    Appends error messages to symbol_table["errors"] for undeclared variables.
    Modifies symbol_table in-place and returns None.
    """
    # Extract node information
    children = node.get("children", [])
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # Ensure errors list exists in symbol_table
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # Ensure variables dict exists in symbol_table
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # Process each print argument
    for child in children:
        _validate_argument(child, symbol_table, line, column)


# === helper functions ===
def _validate_argument(arg_node: AST, symbol_table: SymbolTable, line: int, column: int) -> None:
    """
    Validate a single print argument for undeclared variable references.
    
    Checks if the argument node references a variable and validates declaration.
    Handles nested expressions by recursively checking child nodes.
    """
    arg_type = arg_node.get("type", "")
    
    # Check if this is a variable reference node
    if arg_type == "variable_ref":
        var_name = arg_node.get("name") or arg_node.get("value")
        # Use the variable node's line/column if available, otherwise use parent's
        var_line = arg_node.get("line", line)
        var_column = arg_node.get("column", column)
        if var_name and isinstance(var_name, str):
            _check_variable_declaration(var_name, symbol_table, var_line, var_column)
    
    # Recursively check children for nested variable references
    child_nodes = arg_node.get("children", [])
    for child in child_nodes:
        _validate_argument(child, symbol_table, line, column)


def _check_variable_declaration(var_name: str, symbol_table: SymbolTable, line: int, column: int) -> None:
    """
    Check if a variable is declared in the symbol table.
    
    Appends an error message to symbol_table["errors"] if the variable is not declared.
    """
    variables = symbol_table.get("variables", {})
    
    if var_name not in variables:
        error_msg = f"Error: Variable '{var_name}' used in print without declaration at line {line}, column {column}"
        symbol_table["errors"].append(error_msg)


# === OOP compatibility layer ===
# No OOP wrapper needed - this is a helper function node