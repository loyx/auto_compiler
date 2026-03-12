# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ..evaluate_expression_src import evaluate_expression
from ._validate_binop_expr_package._validate_binop_expr_src import _validate_binop_expr
from ._handle_short_circuit_package._handle_short_circuit_src import _handle_short_circuit
from ._emit_operand_move_package._emit_operand_move_src import _emit_operand_move
from ._handle_arithmetic_package._handle_arithmetic_src import _handle_arithmetic
from ._handle_comparison_package._handle_comparison_src import _handle_comparison

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields (for BINOP):
# {
#   "type": "BINOP",
#   "op": str,
#   "left": dict,
#   "right": dict,
# }

# === main function ===
def _eval_binop(expr: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, str]:
    """Evaluate BINOP expression and generate ARM assembly code."""
    # Validate expression fields
    op, left_expr, right_expr = _validate_binop_expr(expr)
    
    # Evaluate left operand
    left_code, left_delta, left_reg = evaluate_expression(
        left_expr, func_name, label_counter, var_offsets, next_offset
    )
    
    # Evaluate right operand with updated offset
    right_code, right_delta, right_reg = evaluate_expression(
        right_expr, func_name, label_counter, var_offsets, next_offset + left_delta
    )
    
    total_delta = left_delta + right_delta
    code_lines = []
    
    # Handle short-circuit operators
    if op in ("&&", "||"):
        sc_code, sc_label = _handle_short_circuit(op, left_reg, right_reg, func_name, label_counter)
        code_lines.append(sc_code)
        return "\n".join(code_lines), total_delta, "R0"
    
    # Emit operand move instructions
    move_code, _, _ = _emit_operand_move(left_reg, right_reg)
    code_lines.append(move_code)
    
    # Handle arithmetic operators
    if op in ("+", "-", "*", "/"):
        arith_code = _handle_arithmetic(op)
        code_lines.append(arith_code)
        return "\n".join(code_lines), total_delta, "R0"
    
    # Handle comparison operators
    if op in ("==", "!=", "<", ">", "<=", ">="):
        cmp_code = _handle_comparison(op)
        code_lines.append(cmp_code)
        return "\n".join(code_lines), total_delta, "R0"
    
    # Unsupported operator
    raise ValueError(f"Unsupported binary operator: {op}")

# === helper functions ===
# No helper functions - all logic delegated to child functions

# === OOP compatibility layer ===
# Not needed for this function node
