# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration
from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_return_statement_package._handle_return_statement_src import _handle_return_statement
from ._handle_if_statement_package._handle_if_statement_src import _handle_if_statement
from ._handle_while_loop_package._handle_while_loop_src import _handle_while_loop
from ._handle_for_loop_package._handle_for_loop_src import _handle_for_loop
from ._handle_binary_expression_package._handle_binary_expression_src import _handle_binary_expression
from ._handle_unary_expression_package._handle_unary_expression_src import _handle_unary_expression
from ._handle_call_expression_package._handle_call_expression_src import _handle_call_expression
from ._handle_identifier_package._handle_identifier_src import _handle_identifier
from ._handle_literal_package._handle_literal_src import _handle_literal

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
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
    """
    Traverse AST node tree and dispatch to corresponding handler functions.
    
    Args:
        node: AST node with "type" field indicating node type
        symbol_table: Symbol table that may be modified by handlers
    
    Raises:
        ValueError: If node type is unknown
    """
    node_type = node.get("type", "UNKNOWN")
    
    if node_type == "function_declaration":
        _handle_function_declaration(node, symbol_table)
    elif node_type == "variable_declaration":
        _handle_variable_declaration(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "return_statement":
        _handle_return_statement(node, symbol_table)
    elif node_type == "if_statement":
        _handle_if_statement(node, symbol_table)
    elif node_type == "while_loop":
        _handle_while_loop(node, symbol_table)
    elif node_type == "for_loop":
        _handle_for_loop(node, symbol_table)
    elif node_type == "binary_operation":
        _handle_binary_expression(node, symbol_table)
    elif node_type == "unary_operation":
        _handle_unary_expression(node, symbol_table)
    elif node_type == "function_call":
        _handle_call_expression(node, symbol_table)
    elif node_type == "identifier":
        _handle_identifier(node, symbol_table)
    elif node_type == "literal":
        _handle_literal(node, symbol_table)
    else:
        raise ValueError(f"Unknown AST node type: {node_type}")

# === helper functions ===
# No helper functions needed - all logic delegated to handler subfunctions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a plain function node