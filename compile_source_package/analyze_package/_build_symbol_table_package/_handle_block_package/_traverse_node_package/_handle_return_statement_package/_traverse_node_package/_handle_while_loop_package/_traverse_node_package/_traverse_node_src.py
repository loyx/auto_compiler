# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_while_loop_package._handle_while_loop_src import _handle_while_loop
from ._handle_if_stmt_package._handle_if_stmt_src import _handle_if_stmt
from ._handle_for_loop_package._handle_for_loop_src import _handle_for_loop
from ._handle_function_def_package._handle_function_def_src import _handle_function_def
from ._handle_return_stmt_package._handle_return_stmt_src import _handle_return_stmt
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op
from ._handle_unary_op_package._handle_unary_op_src import _handle_unary_op
from ._handle_identifier_package._handle_identifier_src import _handle_identifier
from ._handle_literal_package._handle_literal_src import _handle_literal
from ._handle_function_call_package._handle_function_call_src import _handle_function_call

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "while_loop", "if_stmt", "block", "binary_op", "identifier", "literal", etc.)
#   "children": list,        # 子节点列表 (List[AST])
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int,           # 列号
#   "condition": Any,        # 循环条件表达式 (for while_loop)
#   "body": Any,             # 循环体代码块 (for while_loop)
#   "left": Any,             # 左操作数 (for binary_op)
#   "right": Any,            # 右操作数 (for binary_op)
#   "operator": str,         # 运算符 (for binary_op)
#   "name": str,             # 变量名/函数名 (for identifier)
#   "statements": list,      # 语句列表 (for block)
#   "operand": Any,          # 操作数 (for unary_op)
#   "function": Any,         # 被调用函数 (for function_call)
#   "arguments": list        # 参数列表 (for function_call)
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 [{"error_type", "var_name", "line", "column", "message"}]
# }

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """递归遍历 AST 节点树，根据节点类型分发到对应的处理函数。"""
    node_type = node.get("type", "")
    
    # 根据节点类型分发到对应的处理函数
    if node_type == "while_loop":
        _handle_while_loop(node, symbol_table)
    elif node_type == "if_stmt":
        _handle_if_stmt(node, symbol_table)
    elif node_type == "for_loop":
        _handle_for_loop(node, symbol_table)
    elif node_type == "function_def":
        _handle_function_def(node, symbol_table)
    elif node_type == "return_stmt":
        _handle_return_stmt(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "block":
        _handle_block(node, symbol_table)
    elif node_type == "binary_op":
        _handle_binary_op(node, symbol_table)
    elif node_type == "unary_op":
        _handle_unary_op(node, symbol_table)
    elif node_type == "identifier":
        _handle_identifier(node, symbol_table)
    elif node_type == "literal":
        _handle_literal(node, symbol_table)
    elif node_type == "function_call":
        _handle_function_call(node, symbol_table)
    else:
        # 未知类型：默认遍历 children
        _traverse_children(node, symbol_table)

# === helper functions ===
def _traverse_children(node: AST, symbol_table: SymbolTable) -> None:
    """遍历节点的所有 children 子节点。"""
    children = node.get("children", [])
    for child in children:
        _traverse_node(child, symbol_table)

# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function node.
