# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_function_def_package._handle_function_def_src import _handle_function_def
from ._handle_variable_decl_package._handle_variable_decl_src import _handle_variable_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_statement_package._handle_if_statement_src import _handle_if_statement
from ._handle_while_loop_package._handle_while_loop_src import _handle_while_loop
from ._handle_return_statement_package._handle_return_statement_src import _handle_return_statement

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
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
#   "scope_stack": list            # 作用域栈
# }

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """遍历 AST 节点并分发到对应的处理函数。"""
    node_type = node.get("type", "")
    
    if node_type == "block":
        _handle_block(node, symbol_table)
    elif node_type == "function_def":
        _handle_function_def(node, symbol_table)
    elif node_type == "variable_decl":
        _handle_variable_decl(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "if_statement":
        _handle_if_statement(node, symbol_table)
    elif node_type == "while_loop":
        _handle_while_loop(node, symbol_table)
    elif node_type == "return_statement":
        _handle_return_statement(node, symbol_table)
    # 其他类型静默跳过

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
