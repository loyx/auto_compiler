# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_program_package._handle_program_src import _handle_program
from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_expression_package._handle_expression_src import _handle_expression
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
    """
    AST 递归遍历的调度器。根据 node['type'] 分发到对应的 _handle_* 函数。
    """
    node_type = node.get("type", "")
    
    # 类型分发
    if node_type == "program":
        _handle_program(node, symbol_table)
    elif node_type == "function_declaration":
        _handle_function_declaration(node, symbol_table)
    elif node_type == "block":
        _handle_block(node, symbol_table)
    elif node_type == "variable_declaration":
        _handle_variable_declaration(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "expression":
        _handle_expression(node, symbol_table)
    elif node_type == "identifier":
        _handle_identifier(node, symbol_table)
    elif node_type == "literal":
        _handle_literal(node, symbol_table)
    else:
        # 未知节点类型，记录错误
        line = node.get("line", "?")
        column = node.get("column", "?")
        error_msg = f"Unknown node type '{node_type}' at line {line}, column {column}"
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append({
            "message": error_msg,
            "line": line,
            "column": column,
            "type": "unknown_node"
        })

# === helper functions ===
# No helper functions needed - all logic is in delegated handlers

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a function node, not a framework entry point
