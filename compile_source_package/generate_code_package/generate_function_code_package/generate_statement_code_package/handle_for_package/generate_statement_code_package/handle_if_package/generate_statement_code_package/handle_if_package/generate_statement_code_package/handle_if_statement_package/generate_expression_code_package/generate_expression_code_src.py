# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions - inline implementation

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset for variable
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "op": str,        # binary/unary operator: lt, gt, eq, and, or, not
#   "left": dict,     # left operand (binary ops)
#   "right": dict,    # right operand (binary ops)
#   "operand": dict,  # operand (unary ops)
#   "type": str,      # "literal" or "variable"
#   "value": int,     # literal value
#   "name": str,      # variable name
# }

# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets) -> str:
    """
    Generate ARM assembly code for an expression.
    Result is placed in R0 register.
    """
    # Handle literal
    if expr.get("type") == "literal":
        value = expr["value"]
        return f"    MOV R0, #{value}\n"
    
    # Handle variable
    if expr.get("type") == "variable":
        name = expr["name"]
        offset = var_offsets[name]
        return f"    LDR R0, [FP, #{offset}]\n"
    
    # Handle unary op (not)
    if expr.get("op") == "not":
        operand_code = generate_expression_code(expr["operand"], var_offsets)
        return (
            operand_code +
            "    CMP R0, #0\n"
            "    MOVEQ R0, #1\n"
            "    MOVNE R0, #0\n"
        )
    
    # Handle binary ops
    op = expr.get("op")
    if op in ["lt", "gt", "eq", "and", "or"]:
        left_code = generate_expression_code(expr["left"], var_offsets)
        right_code = generate_expression_code(expr["right"], var_offsets)
        
        # Save left result in R1
        code = left_code
        code += "    MOV R1, R0\n"
        
        # Generate right code (result in R0)
        code += right_code
        
        # Compare and set result
        if op == "lt":
            code += "    CMP R1, R0\n"
            code += "    MOVLT R0, #1\n"
            code += "    MOVGE R0, #0\n"
        elif op == "gt":
            code += "    CMP R1, R0\n"
            code += "    MOVGT R0, #1\n"
            code += "    MOVLE R0, #0\n"
        elif op == "eq":
            code += "    CMP R1, R0\n"
            code += "    MOVEQ R0, #1\n"
            code += "    MOVNE R0, #0\n"
        elif op == "and":
            code += "    AND R0, R1, R0\n"
        elif op == "or":
            code += "    ORR R0, R1, R0\n"
        
        return code
    
    raise ValueError(f"Unknown expression type: {expr}")

# === helper functions ===
# No helper functions needed - all logic in main function

# === OOP compatibility layer ===
# Not needed - this is a pure function node, no framework wrapper required
