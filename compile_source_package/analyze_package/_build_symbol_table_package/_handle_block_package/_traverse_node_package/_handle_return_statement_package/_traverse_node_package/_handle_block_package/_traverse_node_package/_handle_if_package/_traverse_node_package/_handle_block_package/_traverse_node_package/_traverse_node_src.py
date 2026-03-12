# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_function_call_package._handle_function_call_src import _handle_function_call
from ._handle_return_stmt_package._handle_return_stmt_src import _handle_return_stmt
from ._handle_function_def_package._handle_function_def_src import _handle_function_def

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", "return_stmt", "function_def")
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
    AST 遍历的分发中心。根据节点类型调用对应的 handler 函数。
    
    副作用：直接修改 symbol_table（记录变量、函数、作用域、错误等）。
    异常：未知节点类型记录到 errors，不抛出异常。
    """
    node_type = node.get("type", "")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 根据节点类型分发到对应的 handler
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
    elif node_type == "return_stmt":
        _handle_return_stmt(node, symbol_table)
    elif node_type == "function_def":
        _handle_function_def(node, symbol_table)
    else:
        # 未知节点类型，记录错误
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append({
            "type": "unknown_node_type",
            "line": line,
            "column": column,
            "message": f"Unknown AST node type: {node_type}"
        })

# === helper functions ===
# No helper functions needed for this dispatcher

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
