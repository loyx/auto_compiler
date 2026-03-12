# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("binary_op" 或 "operation")
#   "left": AST,             # 左操作数节点
#   "right": AST,            # 右操作数节点
#   "operator": str,         # 运算符 (如 "+", "-", "*", "/", "==", "!=", "<", ">", etc.)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_binary_op(node: AST, symbol_table: SymbolTable) -> str:
    """Handle binary operator node and infer expression type."""
    left_node = node.get("left", {})
    right_node = node.get("right", {})
    operator = node.get("operator", "")
    line = node.get("line", 0)

    # Edge case: empty nodes or operator
    if not left_node or not right_node:
        _record_error(symbol_table, f"missing operand in binary operation at line {line}")
        return "void"
    if not operator:
        _record_error(symbol_table, f"missing operator in binary operation at line {line}")
        return "void"

    # Recursively traverse child nodes to get their types
    left_type = _traverse_node(left_node, symbol_table)
    right_type = _traverse_node(right_node, symbol_table)

    # Propagate void from child errors
    if left_type == "void" or right_type == "void":
        return "void"

    # Type inference based on operator category
    if operator in ["+", "-", "*", "/"]:
        return _handle_arithmetic_op(operator, left_type, right_type, line, symbol_table)
    elif operator in ["==", "!=", "<", ">", "<=", ">="]:
        return _handle_comparison_op(operator, left_type, right_type, line, symbol_table)
    elif operator in ["&&", "||"]:
        return _handle_logical_op(operator, left_type, right_type, line, symbol_table)
    else:
        _record_error(symbol_table, f"unknown operator '{operator}' at line {line}")
        return "void"

# === helper functions ===
def _handle_arithmetic_op(operator: str, left_type: str, right_type: str, line: int, symbol_table: SymbolTable) -> str:
    """Handle arithmetic operators: +, -, *, /"""
    if left_type == "int" and right_type == "int":
        return "int"
    _record_error(symbol_table, f"type mismatch in binary operation '{operator}' at line {line}: '{left_type}' and '{right_type}'")
    return "void"

def _handle_comparison_op(operator: str, left_type: str, right_type: str, line: int, symbol_table: SymbolTable) -> str:
    """Handle comparison operators: ==, !=, <, >, <=, >="""
    if left_type == right_type and left_type in ["int", "char"]:
        return "int"
    _record_error(symbol_table, f"type mismatch in binary operation '{operator}' at line {line}: '{left_type}' and '{right_type}'")
    return "void"

def _handle_logical_op(operator: str, left_type: str, right_type: str, line: int, symbol_table: SymbolTable) -> str:
    """Handle logical operators: &&, ||"""
    if left_type == "int" and right_type == "int":
        return "int"
    _record_error(symbol_table, f"type mismatch in binary operation '{operator}' at line {line}: '{left_type}' and '{right_type}'")
    return "void"

def _record_error(symbol_table: SymbolTable, message: str) -> None:
    """Record error message to symbol table."""
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    symbol_table["errors"].append(message)

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
