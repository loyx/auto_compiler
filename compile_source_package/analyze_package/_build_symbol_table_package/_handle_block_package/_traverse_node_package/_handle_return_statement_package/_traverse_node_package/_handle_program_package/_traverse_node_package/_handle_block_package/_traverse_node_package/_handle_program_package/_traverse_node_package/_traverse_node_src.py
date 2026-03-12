# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_program_package._handle_program_src import _handle_program
from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration
from ._handle_return_statement_package._handle_return_statement_src import _handle_return_statement
from ._handle_expression_statement_package._handle_expression_statement_src import _handle_expression_statement

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
    """递归遍历 AST 节点并根据节点类型分发到对应的 handler 函数。"""
    node_type = node.get("type")
    
    if not node_type:
        return
    
    handler_map = {
        "program": _handle_program,
        "function_declaration": _handle_function_declaration,
        "block": _handle_block,
        "variable_declaration": _handle_variable_declaration,
        "return_statement": _handle_return_statement,
        "expression_statement": _handle_expression_statement,
    }
    
    handler = handler_map.get(node_type)
    
    if handler:
        handler(node, symbol_table)

# === helper functions ===
# No helper functions needed - all logic delegated to handlers

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a plain function node
