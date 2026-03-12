# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions needed; logic is simple enough for inline implementation

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,           # "VAR", "CONST", "BINOP", "UNOP"
#   "value": int,          # value for CONST type
#   "var_name": str,       # variable name for VAR type
#   "op": str,             # operator for BINOP/UNOP
#   "left": Expr,          # left operand for BINOP
#   "right": Expr,         # right operand for BINOP
#   "operand": Expr,       # operand for UNOP
# }

# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate ARM64 assembly code for an expression. Result always in x0."""
    expr_type = expr.get("type")
    
    if expr_type == "VAR":
        var_name = expr["var_name"]
        offset = var_offsets[var_name]
        code = f"ldr x0, [sp, #{offset}]"
        return code, next_offset
    
    elif expr_type == "CONST":
        value = expr["value"]
        if 0 <= value <= 65535:
            code = f"movz x0, #{value}"
        else:
            low16 = value & 0xFFFF
            high16 = (value >> 16) & 0xFFFF
            code = f"movz x0, #{low16}\nmovk x0, #{high16}, lsl #16"
        return code, next_offset
    
    elif expr_type == "UNOP":
        op = expr["op"]
        operand_code, _ = generate_expression_code(expr["operand"], var_offsets, next_offset)
        if op == "-":
            binop_code = "neg x0, x0"
        else:
            binop_code = ""
        code = f"{operand_code}\n{binop_code}"
        return code.strip(), next_offset
    
    elif expr_type == "BINOP":
        op = expr["op"]
        left_code, _ = generate_expression_code(expr["left"], var_offsets, next_offset)
        save_code = "mov x1, x0"
        right_code, _ = generate_expression_code(expr["right"], var_offsets, next_offset)
        
        if op in ["==", "!=", "<", ">", "<=", ">="]:
            cset_map = {"==": "eq", "!=": "ne", "<": "lt", ">": "gt", "<=": "le", ">=": "ge"}
            binop_code = f"cmp x1, x0\ncset x0, {cset_map[op]}"
        else:
            asm_op_map = {"+": "add", "-": "sub", "*": "mul", "/": "sdiv",
                          "&": "and", "|": "orr", "^": "eor"}
            binop_code = f"{asm_op_map[op]} x0, x1, x0"
        
        code = f"{left_code}\n{save_code}\n{right_code}\n{binop_code}"
        return code, next_offset
    
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
