# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_expression_package._handle_expression_src import _handle_expression

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
    """遍历 AST 节点并分发到对应的 handler 函数。"""
    node_type = node.get("type", "")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    handler_map = {
        "if": _handle_if,
        "while": _handle_while,
        "var_decl": _handle_var_decl,
        "assignment": _handle_assignment,
        "block": _handle_block,
        "expression": _handle_expression,
    }
    
    handler = handler_map.get(node_type)
    if handler:
        handler(node, symbol_table)
    else:
        symbol_table.setdefault("errors", []).append({
            "message": "未知节点类型",
            "line": line,
            "column": column,
            "node_type": node_type
        })

# === helper functions ===
# No helper functions needed - all logic delegated to handlers

# === OOP compatibility layer ===
# Not needed for this internal traversal function
