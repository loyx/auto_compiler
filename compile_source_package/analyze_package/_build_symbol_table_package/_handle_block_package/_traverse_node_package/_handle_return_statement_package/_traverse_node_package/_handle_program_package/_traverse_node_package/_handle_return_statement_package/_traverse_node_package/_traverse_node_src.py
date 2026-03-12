# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_program_package._handle_program_src import _handle_program
from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration
from ._handle_function_definition_package._handle_function_definition_src import _handle_function_definition
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_return_statement_package._handle_return_statement_src import _handle_return_statement
from ._handle_if_statement_package._handle_if_statement_src import _handle_if_statement
from ._handle_while_statement_package._handle_while_statement_src import _handle_while_statement
from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration
from ._handle_binary_expression_package._handle_binary_expression_src import _handle_binary_expression
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

HandlerFunc = Any  # Callable[[AST, SymbolTable], None]

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """递归遍历 AST 节点并分发到对应的处理函数。"""
    node_type = node.get("type")
    handler = _get_handler(node_type)
    
    if handler:
        handler(node, symbol_table)
    else:
        # 未知类型：静默跳过，但递归遍历子节点
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)


def _get_handler(node_type: str) -> HandlerFunc:
    """根据节点类型获取对应的处理函数。"""
    handler_map: Dict[str, HandlerFunc] = {
        "program": _handle_program,
        "function_declaration": _handle_function_declaration,
        "function_definition": _handle_function_definition,
        "block": _handle_block,
        "return_statement": _handle_return_statement,
        "if_statement": _handle_if_statement,
        "while_statement": _handle_while_statement,
        "variable_declaration": _handle_variable_declaration,
        "binary_expression": _handle_binary_expression,
        "identifier": _handle_identifier,
        "literal": _handle_literal,
    }
    return handler_map.get(node_type)


# === helper functions ===
# Helper functions are placed after main function.
# _get_handler is defined above as it's called by _traverse_node.

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node.
