# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration
from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration

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
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    Recursively traverse AST nodes and dispatch to appropriate handlers
    based on node type.
    """
    # Base case: None node
    if node is None:
        return
    
    # Get node type
    node_type = node.get("type")
    
    # Get children
    children = node.get("children", [])
    
    # Dispatch to handlers based on node type
    try:
        if node_type == "function_declaration":
            _handle_function_declaration(node, symbol_table)
        elif node_type == "variable_declaration":
            _handle_variable_declaration(node, symbol_table)
        else:
            # Default: traverse children for block, program, or unknown types
            for child in children:
                _traverse_node(child, symbol_table)
    except Exception as e:
        symbol_table["errors"].append({
            "type": "handler_error",
            "message": f"Failed to handle node type '{node_type}': {str(e)}",
            "line": node.get("line"),
            "column": node.get("column")
        })

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node