# === std / third-party imports ===
from typing import Any, Dict, List, Optional

# === sub function imports ===
from .. import _traverse_node
from ._check_arithmetic_operator_package._check_arithmetic_operator_src import _check_arithmetic_operator
from ._check_comparison_operator_package._check_comparison_operator_src import _check_comparison_operator
from ._check_binary_logical_operator_package._check_binary_logical_operator_src import _check_binary_logical_operator
from ._check_unary_logical_operator_package._check_unary_logical_operator_src import _check_unary_logical_operator

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block", "expression" 等)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值 (对于 expression 节点，存储操作符)
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

# === main function ===
def _handle_expression(node: AST, symbol_table: SymbolTable) -> None:
    """处理 expression 类型节点的完整逻辑，包括递归遍历子节点和类型验证。"""
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    operator = node.get("value", "")
    children = node.get("children", [])
    line = node.get("line", 0)
    column = node.get("column", 0)
    current_scope = symbol_table.get("current_scope", 0)
    
    for child in children:
        _traverse_node(child, symbol_table)
    
    operand_types: List[Optional[str]] = [child.get("data_type") for child in children]
    
    if operator in ["+", "-", "*", "/"]:
        _check_arithmetic_operator(operator, operand_types, line, column, current_scope, symbol_table, node)
    elif operator in ["==", "!=", "<", ">", "<=", ">="]:
        _check_comparison_operator(operator, operand_types, line, column, current_scope, symbol_table, node)
    elif operator in ["&&", "||"]:
        _check_binary_logical_operator(operator, operand_types, line, column, current_scope, symbol_table, node)
    elif operator == "!":
        _check_unary_logical_operator(operator, operand_types, line, column, current_scope, symbol_table, node)

# === helper functions ===
# No helper functions in this file; all logic delegated to child functions

# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function node
