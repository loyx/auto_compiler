# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions for this implementation

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "if_else": int,
#   "if_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,  # "CMP", "BINARY_OP", "IDENT", "LITERAL"
#   "op": str,    # "==", "!=", "<", ">", "<=", ">=", "+", "-", "*", "/"
#   "left": dict | int | str,
#   "right": dict | int | str,
#   "value": int,  # for LITERAL
#   "name": str,   # for IDENT
# }

# === main function ===
def generate_expression_code(expr: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for evaluating an expression, result in R0."""
    expr_type = expr.get("type")
    
    if expr_type == "LITERAL":
        return _generate_literal_code(expr, next_offset)
    elif expr_type == "IDENT":
        return _generate_ident_code(expr, var_offsets, next_offset)
    elif expr_type == "BINARY_OP" or expr_type == "CMP":
        return _generate_binary_op_code(expr, label_counter, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
def _generate_literal_code(expr: dict, next_offset: int = 0) -> Tuple[str, int]:
    """Generate code to load a literal value into R0."""
    value = expr["value"]
    code = f"    MOV R0, #{value}\n"
    return code, next_offset

def _generate_ident_code(expr: dict, var_offsets: dict, next_offset: int = 0) -> Tuple[str, int]:
    """Generate code to load a variable from stack into R0."""
    var_name = expr["name"]
    if var_name not in var_offsets:
        raise ValueError(f"Variable '{var_name}' not found in var_offsets")
    offset = var_offsets[var_name]
    code = f"    LDR R0, [SP, #{offset}]\n"
    return code, next_offset

def _generate_binary_op_code(expr: dict, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate code for binary operations (arithmetic or comparison)."""
    op = expr["op"]
    left = expr["left"]
    right = expr["right"]
    
    # Evaluate left operand
    left_code, _ = generate_expression_code(left, "", label_counter, var_offsets, next_offset)
    
    # Push R0 (left result) to stack
    push_code = "    PUSH {R0}\n"
    
    # Evaluate right operand
    right_code, _ = generate_expression_code(right, "", label_counter, var_offsets, next_offset)
    
    # Pop to R1
    pop_code = "    POP {R1}\n"
    
    # Generate operation code
    if op == "+":
        op_code = "    ADD R0, R1, R0\n"
    elif op == "-":
        op_code = "    SUB R0, R1, R0\n"
    elif op == "*":
        op_code = "    MUL R0, R1, R0\n"
    elif op == "/":
        # Division requires special handling; for now use simple pattern
        op_code = "    SDIV R0, R1, R0\n"
    elif op == "==":
        op_code = "    CMP R1, R0\n    MOVEQ R0, #1\n    MOVNE R0, #0\n"
    elif op == "!=":
        op_code = "    CMP R1, R0\n    MOVNE R0, #1\n    MOVEQ R0, #0\n"
    elif op == "<":
        op_code = "    CMP R1, R0\n    MOVLT R0, #1\n    MOVGE R0, #0\n"
    elif op == ">":
        op_code = "    CMP R1, R0\n    MOVGT R0, #1\n    MOVLE R0, #0\n"
    elif op == "<=":
        op_code = "    CMP R1, R0\n    MOVLE R0, #1\n    MOVGT R0, #0\n"
    elif op == ">=":
        op_code = "    CMP R1, R0\n    MOVGE R0, #1\n    MOVLT R0, #0\n"
    else:
        raise ValueError(f"Unknown operator: {op}")
    
    full_code = left_code + push_code + right_code + pop_code + op_code
    return full_code, next_offset

# === OOP compatibility layer ===
# Not needed for this function node
