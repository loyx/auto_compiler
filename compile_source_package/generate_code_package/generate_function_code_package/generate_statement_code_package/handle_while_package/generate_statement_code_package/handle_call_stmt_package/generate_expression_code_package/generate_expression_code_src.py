# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No subfunctions needed - logic is self-contained

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,           # "LITERAL", "VAR", "BINOP", "UNOP"
#   "value": int,          # for LITERAL: the literal value
#   "name": str,           # for VAR: variable name
#   "op": str,             # for BINOP/UNOP: operator (ADD, SUB, MUL, DIV, NEG)
#   "left": Dict,          # for BINOP: left operand expression
#   "right": Dict,         # for BINOP: right operand expression
#   "operand": Dict,       # for UNOP: operand expression
# }

# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate assembly code for an expression, leaving result in x0."""
    expr_type = expr.get("type", "")
    
    if expr_type == "LITERAL":
        value = expr["value"]
        return f"MOV x0, #{value}", next_offset
    
    elif expr_type == "VAR":
        name = expr["name"]
        offset = var_offsets[name]
        return f"LOAD_OFFSET x0, {offset}", next_offset
    
    elif expr_type == "BINOP":
        op = expr["op"]
        left = expr["left"]
        right = expr["right"]
        
        # Generate left operand code (result in x0)
        left_code, next_offset = generate_expression_code(left, var_offsets, next_offset)
        
        # Store left result to temp slot
        temp_offset = next_offset
        next_offset += 8
        store_code = f"STORE_OFFSET {temp_offset}, x0"
        
        # Generate right operand code (result in x0)
        right_code, next_offset = generate_expression_code(right, var_offsets, next_offset)
        
        # Load left result to x1
        load_code = f"LOAD_OFFSET x1, {temp_offset}"
        
        # Perform binary operation
        op_code = f"{op} x0, x1"
        
        full_code = "\n".join([left_code, store_code, right_code, load_code, op_code])
        return full_code, next_offset
    
    elif expr_type == "UNOP":
        op = expr["op"]
        operand = expr["operand"]
        
        # Generate operand code (result in x0)
        operand_code, next_offset = generate_expression_code(operand, var_offsets, next_offset)
        
        # Apply unary operation
        if op == "NEG":
            unop_code = "NEG x0"
        else:
            raise ValueError(f"Unknown unary operator: {op}")
        
        full_code = "\n".join([operand_code, unop_code])
        return full_code, next_offset
    
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No helper functions needed - all logic in main function

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node