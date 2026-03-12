# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_function_call_package._handle_function_call_src import _handle_function_call
from ._handle_function_decl_package._handle_function_decl_src import _handle_function_decl
from ._handle_return_package._handle_return_src import _handle_return
from ._handle_literal_package._handle_literal_src import _handle_literal
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op

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
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    Traverse AST node and dispatch to corresponding handler function.
    
    Input: AST node and symbol table.
    Processing: Dispatch based on node['type'] to _handle_* functions.
    Side effects: May modify symbol_table (variable declarations, scope changes, error collection).
    Exceptions: Does not raise exceptions; errors are recorded to symbol_table['errors'].
    """
    # Handle None node: silently ignore
    if node is None:
        return
    
    # Handle missing 'type' field
    if "type" not in node:
        error_entry = {
            "type": "error",
            "message": "Node missing 'type' field",
            "line": node.get("line", -1),
            "column": node.get("column", -1)
        }
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append(error_entry)
        return
    
    node_type = node["type"]
    
    # Dispatch to corresponding handler
    if node_type == "block":
        _handle_block(node, symbol_table)
    elif node_type == "var_decl":
        _handle_var_decl(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "if":
        _handle_if(node, symbol_table)
    elif node_type == "while":
        _handle_while(node, symbol_table)
    elif node_type == "function_call":
        _handle_function_call(node, symbol_table)
    elif node_type == "function_decl":
        _handle_function_decl(node, symbol_table)
    elif node_type == "return":
        _handle_return(node, symbol_table)
    elif node_type == "literal":
        _handle_literal(node, symbol_table)
    elif node_type == "binary_op":
        _handle_binary_op(node, symbol_table)
    else:
        # Unknown node type: record error
        error_entry = {
            "type": "error",
            "message": f"Unknown node type: {node_type}",
            "line": node.get("line", -1),
            "column": node.get("column", -1)
        }
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append(error_entry)


# === helper functions ===
# No helper functions needed; dispatch logic is in main function

# === OOP compatibility layer ===
# No OOP wrapper needed; this is a plain function node
