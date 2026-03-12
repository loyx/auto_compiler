# === std / third-party imports ===
from typing import Any, Dict, Callable, Optional

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration
from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration
from ._handle_if_statement_package._handle_if_statement_src import _handle_if_statement
from ._handle_while_loop_package._handle_while_loop_src import _handle_while_loop
from ._handle_return_statement_package._handle_return_statement_src import _handle_return_statement
from ._handle_expression_package._handle_expression_src import _handle_expression

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
#   "errors": list                 # 错误列表
# }

HandlerFunc = Callable[[AST, SymbolTable], None]

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """递归遍历 AST 节点，根据类型分发到对应 handler。"""
    node_type = node.get("type", "")
    
    handler_map: Dict[str, HandlerFunc] = {
        "program": _handle_program,
        "block": _handle_block,
        "function_declaration": _handle_function_declaration,
        "variable_declaration": _handle_variable_declaration,
        "if_statement": _handle_if_statement,
        "while_loop": _handle_while_loop,
        "return_statement": _handle_return_statement,
        "expression": _handle_expression,
        "expression_statement": _handle_expression,
    }
    
    handler: Optional[HandlerFunc] = handler_map.get(node_type)
    if handler:
        handler(node, symbol_table)
    else:
        # 未知类型：静默递归 children
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)

# === helper functions ===
def _handle_program(node: AST, symbol_table: SymbolTable) -> None:
    """处理 program 根节点，递归遍历所有子节点。"""
    for child in node.get("children", []):
        _traverse_node(child, symbol_table)

# === OOP compatibility layer ===
# Not required for this function node.
