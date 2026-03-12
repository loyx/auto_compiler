# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_return_package._handle_return_src import _handle_return
from ._handle_function_decl_package._handle_function_decl_src import _handle_function_decl
from ._handle_function_call_package._handle_function_call_src import _handle_function_call
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op
from ._handle_unary_op_package._handle_unary_op_src import _handle_unary_op
from ._handle_literal_package._handle_literal_src import _handle_literal
from ._handle_identifier_package._handle_identifier_src import _handle_identifier

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
    递归遍历 AST 节点并根据节点类型分发到对应的处理函数。
    
    处理逻辑：
    1. 读取 node["type"] 确定节点类型
    2. 根据类型调用相应的处理函数
    3. 对于有 children 的节点，递归遍历所有子节点
    
    副作用：通过 handler 函数修改 symbol_table
    """
    node_type = node.get("type", "")
    
    # Handler 映射表
    handler_map = {
        "block": _handle_block,
        "var_decl": _handle_var_decl,
        "assignment": _handle_assignment,
        "if": _handle_if,
        "while": _handle_while,
        "return": _handle_return,
        "function_decl": _handle_function_decl,
        "function_call": _handle_function_call,
        "binary_op": _handle_binary_op,
        "unary_op": _handle_unary_op,
        "literal": _handle_literal,
        "identifier": _handle_identifier,
    }
    
    # 分发到对应 handler
    handler = handler_map.get(node_type)
    if handler is not None:
        handler(node, symbol_table)
    else:
        # 未知节点类型，记录错误
        error_entry = {
            "type": "unknown_node_type",
            "node_type": node_type,
            "line": node.get("line", -1),
            "column": node.get("column", -1),
            "message": f"Unknown AST node type: {node_type}"
        }
        symbol_table.setdefault("errors", []).append(error_entry)
    
    # 遍历子节点
    children = node.get("children", [])
    for child in children:
        _traverse_node(child, symbol_table)


# === helper functions ===
# No helper functions needed; all logic is in main function


# === OOP compatibility layer ===
# Not needed for this function node
