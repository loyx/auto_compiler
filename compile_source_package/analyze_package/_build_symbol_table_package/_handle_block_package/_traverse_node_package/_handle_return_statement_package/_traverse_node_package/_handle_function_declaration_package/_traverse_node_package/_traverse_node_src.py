# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_statement_package._handle_if_statement_src import _handle_if_statement
from ._handle_while_loop_package._handle_while_loop_src import _handle_while_loop
from ._handle_return_statement_package._handle_return_statement_src import _handle_return_statement
from ._handle_print_statement_package._handle_print_statement_src import _handle_print_statement

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "function_declaration", "variable_declaration", "assignment", etc.)
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
#   "errors": list                 # 错误列表 (List[str])
# }

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """Traverse an AST node and its children, dispatching to appropriate handlers based on node type."""
    # Ensure errors list exists
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    node_type = node.get("type", "")
    
    # Dispatch to handler based on node type
    if node_type == "function_declaration":
        _handle_function_declaration(node, symbol_table)
    elif node_type == "variable_declaration":
        _handle_variable_declaration(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "if_statement":
        _handle_if_statement(node, symbol_table)
    elif node_type == "while_loop":
        _handle_while_loop(node, symbol_table)
    elif node_type == "return_statement":
        _handle_return_statement(node, symbol_table)
    elif node_type == "print_statement":
        _handle_print_statement(node, symbol_table)
    # Unknown types: skip silently
    
    # Auto-traverse children for non-excluded types
    excluded_types = {"program", "block", "if_statement", "while_loop", "function_declaration"}
    if node_type not in excluded_types:
        children = node.get("children", [])
        for child in children:
            _traverse_node(child, symbol_table)

# === helper functions ===
def _handle_function_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """Handle function_declaration nodes: register function in symbol_table and manually traverse children."""
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    if "scope_stack" not in symbol_table:
        symbol_table["scope_stack"] = []
    if "current_scope" not in symbol_table:
        symbol_table["current_scope"] = 0
    
    func_name = node.get("name", "")
    return_type = node.get("return_type", "")
    line = node.get("line", 0)
    column = node.get("column", 0)
    params = node.get("params", [])
    
    # Check for duplicate function declaration
    if func_name in symbol_table["functions"]:
        existing = symbol_table["functions"][func_name]
        symbol_table["errors"].append(
            f"Error: Function '{func_name}' already declared at line {existing['line']}, column {existing['column']}"
        )
        return
    
    # Register function
    symbol_table["functions"][func_name] = {
        "return_type": return_type,
        "params": params,
        "line": line,
        "column": column
    }
    
    # Set current function context
    symbol_table["current_function"] = func_name
    
    # Manually traverse children (params and body)
    children = node.get("children", [])
    for child in children:
        _traverse_node(child, symbol_table)
    
    # Clear current function context
    symbol_table["current_function"] = None

# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function node
