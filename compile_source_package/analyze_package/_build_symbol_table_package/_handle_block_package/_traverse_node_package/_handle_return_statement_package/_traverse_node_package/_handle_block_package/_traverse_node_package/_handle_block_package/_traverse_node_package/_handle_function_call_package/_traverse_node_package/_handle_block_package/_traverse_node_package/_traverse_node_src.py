# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_func_decl_package._handle_func_decl_src import _handle_func_decl
from ._handle_func_call_package._handle_func_call_src import _handle_func_call
from ._handle_return_package._handle_return_src import _handle_return
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op
from ._handle_identifier_package._handle_identifier_src import _handle_identifier
from ._handle_literal_package._handle_literal_src import _handle_literal

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
    """根据 AST 节点类型分发到相应的处理函数。"""
    node_type = node.get("type", "")
    
    handlers = {
        "block": _handle_block,
        "var_decl": _handle_var_decl,
        "assignment": _handle_assignment,
        "if": _handle_if,
        "while": _handle_while,
        "func_decl": _handle_func_decl,
        "func_call": _handle_func_call,
        "return": _handle_return,
        "binary_op": _handle_binary_op,
        "identifier": _handle_identifier,
        "literal": _handle_literal,
    }
    
    handler = handlers.get(node_type)
    if handler:
        handler(node, symbol_table)
    else:
        _handle_unknown_node(node, symbol_table)

# === helper functions ===
def _handle_unknown_node(node: AST, symbol_table: SymbolTable) -> None:
    """处理不支持的节点类型，记录错误。"""
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    line = node.get("line", "?")
    column = node.get("column", "?")
    node_type = node.get("type", "unknown")
    
    symbol_table["errors"].append({
        "type": "unknown_node_type",
        "message": f"不支持的节点类型：{node_type}",
        "line": line,
        "column": column
    })

# === OOP compatibility layer ===
# Not needed for internal traversal function
