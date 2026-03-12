# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions - all logic inline

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": "LITERAL" | "VAR" | "BINOP",
#   "value": int | str,
#   "op": str,
#   "left": dict,
#   "right": dict,
# }

# === main function ===
def evaluate_expression(expr: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """
    Evaluates an expression dictionary into ARM32 assembly code.
    Result is loaded into r0. Returns (assembly_code, updated_next_offset).
    """
    expr_type = expr.get("type")
    
    if expr_type == "LITERAL":
        value = expr.get("value")
        code = f"    mov r0, #{value}\n"
        return code, next_offset
    
    elif expr_type == "VAR":
        var_name = expr.get("value")
        if var_name not in var_offsets:
            raise ValueError(f"Undefined variable: {var_name}")
        offset = var_offsets[var_name]
        code = f"    ldr r0, [sp, #{offset}]\n"
        return code, next_offset
    
    elif expr_type == "BINOP":
        op = expr.get("op")
        left_expr = expr.get("left")
        right_expr = expr.get("right")
        
        # Evaluate left operand
        left_code, offset_after_left = evaluate_expression(left_expr, func_name, label_counter, var_offsets, next_offset)
        
        # Save left result to stack
        save_offset = offset_after_left
        save_code = f"    str r0, [sp, #{save_offset}]\n"
        
        # Evaluate right operand
        right_code, offset_after_right = evaluate_expression(right_expr, func_name, label_counter, var_offsets, save_offset + 1)
        
        # Load left into r1
        load_code = f"    ldr r1, [sp, #{save_offset}]\n"
        
        # Perform operation (r0 = r1 op r0)
        op_map = {
            "add": "add r0, r1, r0",
            "sub": "sub r0, r1, r0",
            "mul": "mul r0, r1, r0",
            "div": "sdiv r0, r1, r0",
        }
        if op not in op_map:
            raise ValueError(f"Unsupported binary operator: {op}")
        op_code = f"    {op_map[op]}\n"
        
        total_code = left_code + save_code + right_code + load_code + op_code
        return total_code, offset_after_right
    
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No helper functions needed - all logic in main

# === OOP compatibility layer ===
# Not needed - this is a pure function node