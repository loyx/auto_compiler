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
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "binary_op", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (如操作符、变量名、字面量值等)
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
    """AST 遍历调度器函数。根据 node['type'] 分发到对应的 handler 函数。"""
    if node is None:
        return
    
    node_type = node.get("type", "")
    
    handler_map = {
        "block": _handle_block,
        "var_decl": _handle_var_decl,
        "assignment": _handle_assignment,
        "if": _handle_if,
        "while": _handle_while,
        "function_call": _handle_function_call,
        "function_decl": _handle_function_decl,
        "return": _handle_return,
        "literal": _handle_literal,
        "binary_op": _handle_binary_op,
    }
    
    handler = handler_map.get(node_type)
    
    if handler is not None:
        handler(node, symbol_table)
    else:
        error_entry = {
            "type": "error",
            "message": f"Unknown node type: {node_type}",
            "line": node.get("line", -1),
            "column": node.get("column", -1)
        }
        symbol_table.setdefault("errors", []).append(error_entry)

# === helper functions ===
# No helper functions needed - all logic delegated to child handlers

# === OOP compatibility layer ===
# Not needed - this is a utility function, not a framework entry point
