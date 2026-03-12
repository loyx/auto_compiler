# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_function_call_package._handle_function_call_src import _handle_function_call
from ._handle_return_package._handle_return_src import _handle_return

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "binary_op", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (对于 binary_op 是运算符字符串)
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
    遍历 AST 节点并根据节点类型分发到相应的处理函数。
    
    处理逻辑：
    1. 根据 node["type"] 判断节点类型
    2. 分发到对应的处理函数
    3. 对于未特殊处理的类型，递归遍历 children
    
    错误处理：
    - 不抛出异常，错误记录在 symbol_table["errors"] 列表中
    """
    node_type = node.get("type", "")
    
    # 分发到对应的处理函数
    if node_type == "binary_op":
        _handle_binary_op(node, symbol_table)
    elif node_type == "var_decl":
        _handle_var_decl(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "if":
        _handle_if(node, symbol_table)
    elif node_type == "while":
        _handle_while(node, symbol_table)
    elif node_type == "block":
        _handle_block(node, symbol_table)
    elif node_type == "function_call":
        _handle_function_call(node, symbol_table)
    elif node_type == "return":
        _handle_return(node, symbol_table)
    else:
        # 对于未特殊处理的节点类型，递归遍历其 children
        _traverse_children(node, symbol_table)

# === helper functions ===
def _traverse_children(node: AST, symbol_table: SymbolTable) -> None:
    """
    递归遍历节点的所有子节点。
    
    用于处理没有专门处理函数的节点类型。
    """
    children = node.get("children", [])
    for child in children:
        if isinstance(child, dict) and "type" in child:
            _traverse_node(child, symbol_table)

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
