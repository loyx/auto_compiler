# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_program_package._handle_program_src import _handle_program
from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration
from ._handle_assignment_statement_package._handle_assignment_statement_src import _handle_assignment_statement
from ._handle_if_statement_package._handle_if_statement_src import _handle_if_statement
from ._handle_while_statement_package._handle_while_statement_src import _handle_while_statement
from ._handle_return_statement_package._handle_return_statement_src import _handle_return_statement
from ._handle_function_call_package._handle_function_call_src import _handle_function_call
from ._handle_identifier_package._handle_identifier_src import _handle_identifier
from ._handle_literal_package._handle_literal_src import _handle_literal

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block" 等)
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
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """递归遍历 AST 节点树，根据节点类型分发到对应的 handler 函数。"""
    node_type = node.get("type", "")
    
    # 分发到对应的 handler
    if node_type == "program":
        _handle_program(node, symbol_table)
    elif node_type == "function_declaration":
        _handle_function_declaration(node, symbol_table)
    elif node_type == "block":
        _handle_block(node, symbol_table)
    elif node_type == "variable_declaration":
        _handle_variable_declaration(node, symbol_table)
    elif node_type == "assignment_statement":
        _handle_assignment_statement(node, symbol_table)
    elif node_type == "if_statement":
        _handle_if_statement(node, symbol_table)
    elif node_type == "while_statement":
        _handle_while_statement(node, symbol_table)
    elif node_type == "return_statement":
        _handle_return_statement(node, symbol_table)
    elif node_type == "function_call":
        _handle_function_call(node, symbol_table)
    elif node_type == "identifier":
        _handle_identifier(node, symbol_table)
    elif node_type == "literal":
        _handle_literal(node, symbol_table)
    else:
        # 未知类型：递归处理 children
        pass
    
    # 递归处理所有子节点
    children = node.get("children", [])
    for child in children:
        _traverse_node(child, symbol_table)

# === helper functions ===
# No helper functions needed - all logic delegated to handlers

# === OOP compatibility layer ===
# Not needed - this is a utility function for static analysis