# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No sub functions delegated

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,           # expression type: "literal", "variable", "binary_op"
#   "value": int,          # literal value (integer only)
#   "name": str,           # variable name
#   "left": dict,          # left operand for binary operations
#   "right": dict,         # right operand for binary operations
#   "op": str,             # operator: "add", "sub", "mul", "div"
# }


# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate ARM64 assembly code for an expression tree node."""
    expr_type = expr.get("type")
    
    if expr_type == "literal":
        value = expr["value"]
        code = f"mov x0, #{value}\n"
        return code, next_offset
    
    elif expr_type == "variable":
        var_name = expr["name"]
        if var_name not in var_offsets:
            raise KeyError(f"Undefined variable: {var_name}")
        offset = var_offsets[var_name]
        code = f"ldr x0, [sp, #{offset}]\n"
        return code, next_offset
    
    elif expr_type == "binary_op":
        op = expr["op"]
        left = expr["left"]
        right = expr["right"]
        
        # Generate code for left operand
        left_code, next_offset = generate_expression_code(left, var_offsets, next_offset)
        
        # Store left result on stack
        store_code = f"str x0, [sp, #{next_offset}]\n"
        left_slot = next_offset
        next_offset += 1
        
        # Generate code for right operand
        right_code, next_offset = generate_expression_code(right, var_offsets, next_offset)
        
        # Move right result to x1
        move_code = "mov x1, x0\n"
        
        # Load left result from stack
        load_code = f"ldr x0, [sp, #{left_slot}]\n"
        
        # Map operator to ARM64 instruction
        op_map = {
            "add": "add",
            "sub": "sub",
            "mul": "mul",
            "div": "sdiv"
        }
        if op not in op_map:
            raise ValueError(f"Unsupported operator: {op}")
        asm_op = op_map[op]
        
        # Perform operation
        op_code = f"{asm_op} x0, x0, x1\n"
        
        # Combine all code
        code = left_code + store_code + right_code + move_code + load_code + op_code
        
        # Stack slot reclaimed (decrement next_offset)
        next_offset -= 1
        
        return code, next_offset
    
    else:
        raise ValueError(f"Unsupported expression type: {expr_type}")


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
