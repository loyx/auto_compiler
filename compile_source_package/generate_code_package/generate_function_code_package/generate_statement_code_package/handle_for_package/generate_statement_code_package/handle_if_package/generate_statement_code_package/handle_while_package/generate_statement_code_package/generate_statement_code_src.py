# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .handle_while_stmt_package.handle_while_stmt_src import handle_while_stmt
from .handle_if_stmt_package.handle_if_stmt_src import handle_if_stmt
from .handle_assign_stmt_package.handle_assign_stmt_src import handle_assign_stmt
from .handle_return_stmt_package.handle_return_stmt_src import handle_return_stmt
from .handle_expr_stmt_package.handle_expr_stmt_src import handle_expr_stmt

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "if_else": int,
#   "if_end": int,
#   "while_start": int,
#   "while_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,  # "while", "if", "assign", "return", "expr_stmt"
#   "condition": dict,  # for while/if
#   "body": list,  # for while/if
#   "else_body": list,  # for if
#   "variable": str,  # for assign
#   "value": dict,  # for assign
#   "expression": dict,  # for expr_stmt
#   "return_value": dict,  # for return
# }

# === main function ===
def generate_statement_code(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for a single statement by dispatching to type-specific handlers."""
    stmt_type = stmt.get("type", "")
    
    if stmt_type == "while":
        return handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "if":
        return handle_if_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "assign":
        return handle_assign_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "return":
        return handle_return_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "expr_stmt":
        return handle_expr_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown statement type: {stmt_type}")

# === helper functions ===
# No helper functions needed - all logic delegated to child handlers

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a function node in the dependency tree