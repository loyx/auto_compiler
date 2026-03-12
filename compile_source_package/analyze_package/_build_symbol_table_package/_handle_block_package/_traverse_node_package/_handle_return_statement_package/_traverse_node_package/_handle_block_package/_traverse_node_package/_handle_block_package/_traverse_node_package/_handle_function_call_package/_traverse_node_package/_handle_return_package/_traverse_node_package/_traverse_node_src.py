# === std / third-party imports ===
from typing import Any, Dict, Callable, Optional

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_return_package._handle_return_src import _handle_return
from ._handle_function_call_package._handle_function_call_src import _handle_function_call
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op
from ._handle_unary_op_package._handle_unary_op_src import _handle_unary_op
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

HandlerFunc = Callable[[AST, SymbolTable], None]

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    遍历 AST 节点及其子节点，根据节点类型分发到相应的 handler 函数。
    
    处理步骤：
    1. 获取节点的 "type" 字段
    2. 根据 type 值分发到对应的 handler 函数
    3. 如果节点有 children，递归遍历每个子节点
    4. 对于未知类型的节点，记录错误并跳过
    """
    node_type = node.get("type", "")
    
    # 获取对应的 handler 函数
    handler = _get_handler(node_type)
    
    # 调用 handler 处理当前节点
    if handler is not None:
        handler(node, symbol_table)
    else:
        # 未知节点类型，记录错误
        _handle_unknown_node(node, symbol_table)
    
    # 递归遍历子节点
    children = node.get("children", [])
    for child in children:
        _traverse_node(child, symbol_table)

# === helper functions ===
def _get_handler(node_type: str) -> Optional[HandlerFunc]:
    """根据节点类型获取对应的 handler 函数。"""
    handler_map: Dict[str, HandlerFunc] = {
        "block": _handle_block,
        "var_decl": _handle_var_decl,
        "assignment": _handle_assignment,
        "if": _handle_if,
        "while": _handle_while,
        "return": _handle_return,
        "function_call": _handle_function_call,
        "binary_op": _handle_binary_op,
        "unary_op": _handle_unary_op,
        "identifier": _handle_identifier,
        "literal": _handle_literal,
    }
    return handler_map.get(node_type)


def _handle_unknown_node(node: AST, symbol_table: SymbolTable) -> None:
    """处理未知类型的节点，记录错误信息。"""
    line = node.get("line", 0)
    column = node.get("column", 0)
    node_type = node.get("type", "<unknown>")
    
    error_msg = f"Unknown node type '{node_type}' at line {line}, column {column}"
    
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    symbol_table["errors"].append({
        "message": error_msg,
        "line": line,
        "column": column,
        "type": "unknown_node"
    })

# === OOP compatibility layer ===
# Not needed for this helper function node
