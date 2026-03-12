# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions needed - this is a leaf node

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # Maps variable name to stack offset
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,  # "LITERAL" | "IDENT" | "BINARY" | "UNARY"
#   "value": int,  # For LITERAL: the integer value
#   "name": str,  # For IDENT: the variable name
#   "op": str,  # For BINARY/UNARY: the operator
#   "left": Expr,  # For BINARY: left operand expression
#   "right": Expr,  # For BINARY: right operand expression
#   "expr": Expr,  # For UNARY: the operand expression
# }

# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """Generate assembly code for evaluating an expression."""
    expr_type = expr["type"]
    
    if expr_type == "LITERAL":
        value = expr["value"]
        reg = f"R{next_offset}"
        code = f"    LOAD_IMM {reg}, {value}\n"
        return code, next_offset + 1, reg
    
    elif expr_type == "IDENT":
        name = expr["name"]
        offset = var_offsets[name]
        reg = f"R{next_offset}"
        code = f"    LOAD_STACK {reg}, {offset}\n"
        return code, next_offset + 1, reg
    
    elif expr_type == "BINARY":
        op = expr["op"]
        left_expr = expr["left"]
        right_expr = expr["right"]
        
        # Generate code for left operand
        left_code, next_offset, left_reg = generate_expression_code(left_expr, var_offsets, next_offset)
        
        # Generate code for right operand
        right_code, next_offset, right_reg = generate_expression_code(right_expr, var_offsets, next_offset)
        
        # Perform binary operation
        result_reg = f"R{next_offset}"
        bin_code = f"    {op} {result_reg}, {left_reg}, {right_reg}\n"
        
        return left_code + right_code + bin_code, next_offset + 1, result_reg
    
    elif expr_type == "UNARY":
        op = expr["op"]
        operand_expr = expr["expr"]
        
        # Generate code for operand
        operand_code, next_offset, operand_reg = generate_expression_code(operand_expr, var_offsets, next_offset)
        
        # Perform unary operation
        result_reg = f"R{next_offset}"
        unary_code = f"    {op} {result_reg}, {operand_reg}\n"
        
        return operand_code + unary_code, next_offset + 1, result_reg
    
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed - this is a utility function, not a framework entry point