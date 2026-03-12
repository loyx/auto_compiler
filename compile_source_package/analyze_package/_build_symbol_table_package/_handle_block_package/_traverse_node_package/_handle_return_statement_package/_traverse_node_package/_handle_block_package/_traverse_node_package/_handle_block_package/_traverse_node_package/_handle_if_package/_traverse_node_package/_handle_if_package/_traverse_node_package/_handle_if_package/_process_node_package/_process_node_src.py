# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_for_package._handle_for_src import _handle_for
from ._handle_function_def_package._handle_function_def_src import _handle_function_def
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op
from ._handle_unary_op_package._handle_unary_op_src import _handle_unary_op
from ._handle_identifier_package._handle_identifier_src import _handle_identifier
from ._handle_literal_package._handle_literal_src import _handle_literal

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "data_type": str,
#   "line": int,
#   "column": int
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
def _process_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    通用 AST 节点分发处理函数。
    
    根据 node 的 "type" 字段分发到对应的 _handle_* 函数。
    所有错误记录到 symbol_table["errors"]，不抛出异常。
    """
    node_type = node.get("type", "")
    
    handler_map = {
        "if": _handle_if,
        "while": _handle_while,
        "for": _handle_for,
        "function_def": _handle_function_def,
        "block": _handle_block,
        "assignment": _handle_assignment,
        "binary_op": _handle_binary_op,
        "unary_op": _handle_unary_op,
        "identifier": _handle_identifier,
        "literal": _handle_literal,
    }
    
    handler = handler_map.get(node_type)
    
    if handler is not None:
        try:
            handler(node, symbol_table)
        except Exception as e:
            error_msg = {
                "type": "handler_error",
                "message": str(e),
                "node_type": node_type,
                "line": node.get("line"),
                "column": node.get("column")
            }
            symbol_table.setdefault("errors", []).append(error_msg)
    else:
        error_msg = {
            "type": "unknown_node_type",
            "message": f"Unknown AST node type: {node_type}",
            "line": node.get("line"),
            "column": node.get("column")
        }
        symbol_table.setdefault("errors", []).append(error_msg)

# === helper functions ===
# No helper functions needed - all logic delegated to child handlers

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a function dependency tree node