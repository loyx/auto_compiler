# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration
from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_statement_package._handle_if_statement_src import _handle_if_statement
from ._handle_while_loop_package._handle_while_loop_src import _handle_while_loop
from ._handle_for_loop_package._handle_for_loop_src import _handle_for_loop
from ._handle_return_statement_package._handle_return_statement_src import _handle_return_statement
from ._handle_expression_statement_package._handle_expression_statement_src import _handle_expression_statement

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "name": str,             # 函数名
#   "params": list,          # 参数列表
#   "body": AST,             # 函数体
#   "return_type": str,      # 返回类型
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,
#   "scope_stack": list
# }

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """递归遍历 AST 节点，根据节点类型分发到相应的处理函数。"""
    node_type = node.get("type")
    
    if node_type == "function_declaration":
        _handle_function_declaration(node, symbol_table)
    elif node_type == "variable_declaration":
        _handle_variable_declaration(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "if_statement":
        _handle_if_statement(node, symbol_table)
    elif node_type == "while_loop":
        _handle_while_loop(node, symbol_table)
    elif node_type == "for_loop":
        _handle_for_loop(node, symbol_table)
    elif node_type == "return_statement":
        _handle_return_statement(node, symbol_table)
    elif node_type == "expression_statement":
        _handle_expression_statement(node, symbol_table)
    elif node_type == "block":
        for stmt in node.get("statements", []):
            _traverse_node(stmt, symbol_table)
    else:
        pass  # 未知类型，静默跳过

# === helper functions ===
# No helper functions needed for this dispatcher

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
