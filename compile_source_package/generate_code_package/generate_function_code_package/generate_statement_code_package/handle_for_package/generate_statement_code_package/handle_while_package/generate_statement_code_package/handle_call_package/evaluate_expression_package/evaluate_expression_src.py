# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions needed - logic is self-contained

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name mapped to stack offset
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": "VAR" | "CONST" | "BINOP",
#   "name": str,        # for VAR: variable name
#   "value": int,       # for CONST: constant value
#   "op": str,          # for BINOP: operation (ADD, SUB, MUL, DIV, AND, ORR, EOR, LSL, LSR, CMP)
#   "left": Expr,       # for BINOP: left operand expression
#   "right": Expr,      # for BINOP: right operand expression
# }

# === main function ===
def evaluate_expression(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """
    Evaluate a single expression and generate ARM32 assembly code.
    
    Returns:
        Tuple[assembly_code, updated_offset, result_register]
        - assembly_code: Generated ARM32 instructions
        - updated_offset: Next available stack offset after evaluation
        - result_register: Register containing result (always "r0")
    """
    expr_type = expr["type"]
    lines = []
    
    if expr_type == "CONST":
        value = expr["value"]
        lines.append(f"    mov r0, #{value}")
        return ("\n".join(lines), next_offset, "r0")
    
    elif expr_type == "VAR":
        name = expr["name"]
        if name not in var_offsets:
            raise KeyError(f"Undefined variable: {name}")
        offset = var_offsets[name]
        lines.append(f"    ldr r0, [sp, #{offset}]")
        return ("\n".join(lines), next_offset, "r0")
    
    elif expr_type == "BINOP":
        op = expr["op"]
        left_expr = expr["left"]
        right_expr = expr["right"]
        
        # Map operation to ARM32 instruction
        op_map = {
            "ADD": "add",
            "SUB": "sub",
            "MUL": "mul",
            "DIV": "sdiv",
            "AND": "and",
            "ORR": "orr",
            "EOR": "eor",
            "LSL": "lsl",
            "LSR": "lsr",
            "CMP": "cmp",
        }
        
        if op not in op_map:
            raise ValueError(f"Unknown operation: {op}")
        
        asm_op = op_map[op]
        
        # Evaluate left operand
        left_code, left_offset, _ = evaluate_expression(left_expr, var_offsets, next_offset)
        lines.append(left_code)
        
        # Save left result to stack
        lines.append(f"    str r0, [sp, #{left_offset}]")
        
        # Evaluate right operand
        right_code, right_offset, _ = evaluate_expression(right_expr, var_offsets, left_offset + 4)
        lines.append(right_code)
        
        # Load left operand into r1, perform operation
        lines.append(f"    ldr r1, [sp, #{left_offset}]")
        lines.append(f"    {asm_op} r0, r1, r0")
        
        return ("\n".join(lines), right_offset, "r0")
    
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node
