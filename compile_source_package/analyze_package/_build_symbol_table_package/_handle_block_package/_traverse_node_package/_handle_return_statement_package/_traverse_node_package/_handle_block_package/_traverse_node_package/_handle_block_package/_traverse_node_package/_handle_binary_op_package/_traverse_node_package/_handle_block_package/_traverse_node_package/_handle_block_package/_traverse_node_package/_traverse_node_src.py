# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "binary_op", "literal", "identifier", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (如操作符、变量名、字面量值等)
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
    
    输入：AST 节点和符号表
    处理：根据 node['type'] 调用相应的 _handle_* 函数
    副作用：可能修改 symbol_table（记录变量、函数、错误等）
    异常：不抛出异常，所有错误记录到 symbol_table['errors']
    """
    # 检查 node 是否有 "type" 字段
    if "type" not in node:
        error_msg = f"AST node missing 'type' field at line {node.get('line', 'unknown')}, column {node.get('column', 'unknown')}"
        symbol_table.setdefault("errors", []).append(error_msg)
        return
    
    node_type = node["type"]
    
    # 根据节点类型分发到对应处理函数
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
    elif node_type == "binary_op":
        _handle_binary_op(node, symbol_table)
    elif node_type == "literal":
        # 字面量节点无需特殊处理
        pass
    elif node_type == "identifier":
        # 标识符节点无需特殊处理
        pass
    else:
        # 未知节点类型，记录错误
        error_msg = f"Unknown AST node type '{node_type}' at line {node.get('line', 'unknown')}, column {node.get('column', 'unknown')}"
        symbol_table.setdefault("errors", []).append(error_msg)

# === helper functions ===
# No helper functions needed - all logic delegated to sub-functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a helper function node, not a framework entry point
