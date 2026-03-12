# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "expression", "binary_op", "literal", "identifier", etc.)
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
    """AST 遍历分发器：根据 node['type'] 分发到对应的 handler 函数。"""
    node_type = node.get("type", "")
    children = node.get("children", [])

    if node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "var_decl":
        _handle_var_decl(node, symbol_table)
    elif node_type == "if":
        _handle_if(node, symbol_table)
    elif node_type == "while":
        _handle_while(node, symbol_table)
    elif node_type == "block":
        for child in children:
            _traverse_node(child, symbol_table)
    elif node_type in ("binary_op", "literal", "identifier", "expression"):
        for child in children:
            _traverse_node(child, symbol_table)
    else:
        # 默认处理：遍历所有子节点
        for child in children:
            _traverse_node(child, symbol_table)


# === helper functions ===
# No helper functions needed for this dispatcher


# === OOP compatibility layer ===
# No OOP wrapper needed for internal AST traversal function
