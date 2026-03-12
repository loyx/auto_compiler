# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_declaration_package._handle_declaration_src import _handle_declaration
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_function_call_package._handle_function_call_src import _handle_function_call

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("block", "declaration", "assignment", "function_call", etc.)
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
    遍历 AST 节点并根据节点类型分发到对应的处理函数。
    
    根据 node["type"] 调用相应的处理函数：
    - "block" -> _handle_block
    - "declaration" -> _handle_declaration
    - "assignment" -> _handle_assignment
    - "function_call" -> _handle_function_call
    
    不支持的类型会记录到 symbol_table["errors"] 中。
    """
    node_type = node.get("type", "")
    
    if node_type == "block":
        _handle_block(node, symbol_table)
    elif node_type == "declaration":
        _handle_declaration(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "function_call":
        _handle_function_call(node, symbol_table)
    else:
        # 不支持的节点类型，记录警告（可选）
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        line = node.get("line", -1)
        column = node.get("column", -1)
        symbol_table["errors"].append({
            "type": "unknown_node_type",
            "message": f"Unsupported node type: {node_type}",
            "line": line,
            "column": column
        })


# === helper functions ===
# No helper functions needed - all logic delegated to child handlers

# === OOP compatibility layer ===
# Not needed for internal traversal function