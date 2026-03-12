# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_binop_package.generate_binop_src import generate_binop
from .generate_unop_package.generate_unop_src import generate_unop

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_end": int,
#   "if_end": int,
#   "if_else": int,
#   "and": int,
#   "or": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,  # e.g., "CONST", "VAR", "BINOP", "UNOP", "CALL"
#   "value": Any,  # for CONST
#   "var_name": str,  # for VAR
#   "op": str,  # for BINOP/UNOP
#   "left": dict,  # for BINOP
#   "right": dict,  # for BINOP
#   "operand": dict,  # for UNOP
#   "func_name": str,  # for CALL
#   "args": list,  # for CALL
# }


# === main function ===
def evaluate_expression(expr: Expr, func_name: str, label_counter: LabelCounter, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate ARM32 assembly code to evaluate an expression. Result in r0."""
    expr_type = expr.get("type")
    
    if expr_type == "CONST":
        value = expr["value"]
        code = f"ldr r0, ={value}\n"
        return code, next_offset
    
    elif expr_type == "VAR":
        var_name = expr["var_name"]
        offset = var_offsets[var_name]
        code = f"ldr r0, [sp, #{offset}]\n"
        return code, next_offset
    
    elif expr_type == "BINOP":
        op = expr["op"]
        left_code, offset = evaluate_expression(expr["left"], func_name, label_counter, var_offsets, next_offset)
        right_code, offset = evaluate_expression(expr["right"], func_name, label_counter, var_offsets, offset)
        
        code = left_code
        code += "push {r0}\n"
        code += right_code
        code += "pop {r1}\n"
        code += generate_binop(op, label_counter)
        return code, offset
    
    elif expr_type == "UNOP":
        op = expr["op"]
        operand_code, offset = evaluate_expression(expr["operand"], func_name, label_counter, var_offsets, next_offset)
        code = operand_code
        code += generate_unop(op)
        return code, offset
    
    elif expr_type == "CALL":
        func_name_call = expr["func_name"]
        args = expr.get("args", [])
        code = ""
        offset = next_offset
        
        for arg in reversed(args):
            arg_code, offset = evaluate_expression(arg, func_name, label_counter, var_offsets, offset)
            code += arg_code
            code += "push {r0}\n"
        
        code += f"bl {func_name_call}\n"
        if args:
            code += f"add sp, sp, #{len(args) * 4}\n"
        return code, offset
    
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")


# === helper functions ===
# No inline helpers - delegated to child functions

# === OOP compatibility layer ===
# Not needed - this is a pure function node