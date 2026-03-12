# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_function_call_package._handle_function_call_src import _handle_function_call
from ._handle_return_package._handle_return_src import _handle_return

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
    递归遍历 AST 节点的核心分发器。
    
    根据 node["type"] 分发到对应的 handler 子函数。
    所有错误记录到 symbol_table["errors"]，不抛出异常。
    """
    node_type = node.get("type")
    
    if not node_type:
        return
    
    handler_map = {
        "block": _handle_block,
        "var_decl": _handle_var_decl,
        "assignment": _handle_assignment,
        "if": _handle_if,
        "while": _handle_while,
        "function_call": _handle_function_call,
        "return": _handle_return,
    }
    
    handler = handler_map.get(node_type)
    
    if handler:
        handler(node, symbol_table)
    else:
        # 未知节点类型，静默处理或记录警告
        line = node.get("line", "?")
        column = node.get("column", "?")
        symbol_table.setdefault("errors", []).append({
            "type": "warning",
            "message": f"Unknown node type: {node_type}",
            "line": line,
            "column": column
        })

# === helper functions ===
# No helper functions needed - all logic delegated to handlers

# === OOP compatibility layer ===
# Not needed for this function node