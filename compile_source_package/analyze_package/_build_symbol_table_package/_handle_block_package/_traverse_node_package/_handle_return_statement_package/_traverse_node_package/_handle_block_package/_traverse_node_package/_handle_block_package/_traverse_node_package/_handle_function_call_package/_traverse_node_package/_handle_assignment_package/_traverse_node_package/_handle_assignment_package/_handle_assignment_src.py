# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions for this module

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "assignment", "var_decl", "if", "while", "block", "binary_op", "literal", "identifier", "expression", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "target": str,           # 赋值目标变量名 (可选)
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
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle assignment statement node for semantic analysis.
    
    Checks if the target variable is declared. If not, records an error.
    Traverses child nodes for further processing.
    
    Side effects: May modify symbol_table["errors"]
    """
    # Extract variable name from target
    var_name = _extract_target_variable(node)
    
    # Get line and column for error reporting
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # Check if variable is declared
    if var_name and not _is_variable_declared(var_name, symbol_table):
        # Record error for undefined variable
        _record_undefined_variable_error(var_name, line, column, symbol_table)
    
    # Traverse child nodes for expression processing
    _traverse_children(node, symbol_table)

# === helper functions ===
def _extract_target_variable(node: AST) -> str:
    """Extract the target variable name from assignment node."""
    # Try to get from "target" field first
    if "target" in node:
        target = node["target"]
        if isinstance(target, str):
            return target
        elif isinstance(target, dict) and target.get("type") == "identifier":
            return target.get("value", "")
    
    # Try to find identifier in children
    children = node.get("children", [])
    for child in children:
        if isinstance(child, dict) and child.get("type") == "identifier":
            return child.get("value", "")
    
    return ""

def _is_variable_declared(var_name: str, symbol_table: SymbolTable) -> bool:
    """Check if a variable is declared in the symbol table."""
    variables = symbol_table.get("variables", {})
    if var_name not in variables:
        return False
    
    var_info = variables[var_name]
    return var_info.get("is_declared", False)

def _record_undefined_variable_error(var_name: str, line: int, column: int, symbol_table: SymbolTable) -> None:
    """Record an undefined variable error to the symbol table."""
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    error = {
        "error": "undefined variable",
        "name": var_name,
        "line": line,
        "column": column
    }
    symbol_table["errors"].append(error)

def _traverse_children(node: AST, symbol_table: SymbolTable) -> None:
    """Traverse child nodes for further semantic analysis."""
    children = node.get("children", [])
    for child in children:
        if isinstance(child, dict):
            # Child nodes will be processed by their respective handlers
            # This is a placeholder for recursive traversal logic
            pass

# === OOP compatibility layer ===
# Not needed for this function node
