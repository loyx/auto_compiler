# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_program_package._handle_program_src import _handle_program
from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration
from ._handle_block_package._handle_block_src import _handle_block
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
    """递归遍历 AST 节点进行语义检查。这是语义分析的主分发函数。"""
    # 防御性初始化 symbol_table
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    if "current_scope" not in symbol_table:
        symbol_table["current_scope"] = 0
    if "scope_stack" not in symbol_table:
        symbol_table["scope_stack"] = []

    node_type = node.get("type", "")

    # 根据节点类型分发到对应的 handler
    if node_type == "program":
        _handle_program(node, symbol_table)
    elif node_type == "function_declaration":
        _handle_function_declaration(node, symbol_table)
    elif node_type == "block":
        _handle_block(node, symbol_table)
    elif node_type == "expression":
        _handle_expression(node, symbol_table)
    elif node_type == "identifier":
        _handle_identifier(node, symbol_table)
    elif node_type == "literal":
        _handle_literal(node, symbol_table)
    else:
        # 未知节点类型：递归遍历子节点
        children = node.get("children", [])
        if children:
            for child in children:
                _traverse_node(child, symbol_table)


# === helper functions ===
# No helper functions needed for this dispatcher

# === OOP compatibility layer ===
# Not needed for this function node
