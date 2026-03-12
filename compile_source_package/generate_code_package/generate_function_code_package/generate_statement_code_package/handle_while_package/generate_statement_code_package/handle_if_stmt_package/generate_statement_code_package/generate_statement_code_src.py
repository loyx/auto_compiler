# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .handle_if_stmt_package.handle_if_stmt_src import handle_if_stmt
from .handle_while_stmt_package.handle_while_stmt_src import handle_while_stmt
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_end": int,
#   "if_else": int,
#   "if_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,           # "assign", "if", "while", "return", "expr_stmt"
#   "target": str,         # variable name for assignment
#   "value": dict,         # expression for assignment value
#   "condition": dict,     # condition for if/while
#   "then_body": list,     # then body for if
#   "else_body": list,     # else body for if (optional)
#   "body": list,          # body statements for while
#   "expression": dict,    # expression for expr_stmt
#   "return_value": dict,  # return value expression
# }

# === main function ===
def generate_statement_code(stmt: Stmt, func_name: str, label_counter: LabelCounter, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate assembly code for a single statement by dispatching to handlers."""
    stmt_type = stmt.get("type")
    
    if stmt_type == "assign":
        return _handle_assign(stmt, var_offsets, next_offset)
    elif stmt_type == "if":
        return handle_if_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "while":
        return handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "return":
        return _handle_return(stmt, next_offset)
    elif stmt_type == "expr_stmt":
        return _handle_expr_stmt(stmt, next_offset)
    else:
        raise ValueError(f"Unknown statement type: {stmt_type}")

# === helper functions ===
def _handle_assign(stmt: Stmt, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Handle variable assignment: compute value, store to stack."""
    value_expr = stmt["value"]
    target = stmt["target"]
    
    code, new_offset = generate_expression_code(value_expr, var_offsets, next_offset)
    offset = var_offsets[target]
    code += f"STR x0, [sp, #{offset}]\n"
    return code, new_offset

def _handle_return(stmt: Stmt, next_offset: int) -> Tuple[str, int]:
    """Handle return statement: compute value, result already in x0."""
    return_value = stmt.get("return_value") or stmt.get("value")
    if return_value:
        code, new_offset = generate_expression_code(return_value, {}, next_offset)
        return code, new_offset
    return "", next_offset

def _handle_expr_stmt(stmt: Stmt, next_offset: int) -> Tuple[str, int]:
    """Handle expression statement: compute expression, discard result."""
    expr = stmt["expression"]
    code, new_offset = generate_expression_code(expr, {}, next_offset)
    return code, new_offset

# === OOP compatibility layer ===
