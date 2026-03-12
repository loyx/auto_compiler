# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions - inline implementation

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name to stack offset mapping
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,  # "literal", "variable", "binary_op", "unary_op"
#   "value": Any,  # for literal: int/float constant value
#   "var_name": str,  # for variable: variable identifier
#   "operator": str,  # for binary_op/unary_op: "+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">=", "not"
#   "left": dict,  # for binary_op: left operand Expr
#   "right": dict,  # for binary_op: right operand Expr
#   "operand": dict,  # for unary_op: single operand Expr
# }

# === main function ===
def generate_expression_code(expr: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, int]:
    """Generate ARM assembly code to evaluate an expression with result in R0."""
    expr_type = expr.get("type")
    
    if expr_type == "literal":
        return _generate_literal_code(expr, next_offset)
    elif expr_type == "variable":
        return _generate_variable_code(expr, var_offsets, next_offset)
    elif expr_type == "binary_op":
        return _generate_binary_op_code(expr, var_offsets, next_offset)
    elif expr_type == "unary_op":
        return _generate_unary_op_code(expr, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
def _generate_literal_code(expr: dict, next_offset: int) -> Tuple[str, int, int]:
    """Generate code for literal constant."""
    value = expr.get("value")
    
    if isinstance(value, int) and 0 <= value <= 255:
        asm = f"MOV R0, #{value}\n"
    else:
        asm = f"LDR R0, ={value}\n"
    
    return asm, 0, next_offset

def _generate_variable_code(expr: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, int]:
    """Generate code for variable reference."""
    var_name = expr.get("var_name")
    
    if var_name not in var_offsets:
        raise ValueError(f"Undefined variable: {var_name}")
    
    offset = var_offsets[var_name]
    asm = f"LDR R0, [SP, #{offset}]\n"
    
    return asm, 0, next_offset

def _generate_binary_op_code(expr: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, int]:
    """Generate code for binary operation."""
    operator = expr.get("operator")
    left = expr.get("left")
    right = expr.get("right")
    
    # Evaluate left operand
    left_asm, _, offset_after_left = generate_expression_code(left, var_offsets, next_offset)
    
    # Save left result to temp stack
    temp_offset = offset_after_left
    offset_after_save = temp_offset + 4
    save_asm = f"STR R0, [SP, #{temp_offset}]\n"
    
    # Evaluate right operand
    right_asm, _, offset_after_right = generate_expression_code(right, var_offsets, offset_after_save)
    
    # Load left operand into R1
    load_asm = f"LDR R1, [SP, #{temp_offset}]\n"
    
    # Generate operation code
    op_asm = _generate_binary_operation(operator)
    
    total_asm = left_asm + save_asm + right_asm + load_asm + op_asm
    return total_asm, 0, offset_after_right

def _generate_binary_operation(operator: str) -> str:
    """Generate ARM instruction for binary operation."""
    op_map = {
        "+": "ADD R0, R1, R0\n",
        "-": "SUB R0, R1, R0\n",
        "*": "MUL R0, R1, R0\n",
        "/": "SDIV R0, R1, R0\n",
    }
    
    if operator in op_map:
        return op_map[operator]
    
    # Comparison operations - produce boolean 0/1
    cmp_asm = "CMP R1, R0\n"
    cmp_ops = {
        "==": "MOVEQ R0, #1\nMOVNE R0, #0\n",
        "!=": "MOVNE R0, #1\nMOVEQ R0, #0\n",
        "<": "MOVLT R0, #1\nMOVGE R0, #0\n",
        ">": "MOVGT R0, #1\nMOVLE R0, #0\n",
        "<=": "MOVLE R0, #1\nMOVGT R0, #0\n",
        ">=": "MOVGE R0, #1\nMOVLT R0, #0\n",
    }
    
    if operator in cmp_ops:
        return cmp_asm + cmp_ops[operator]
    
    raise ValueError(f"Unknown binary operator: {operator}")

def _generate_unary_op_code(expr: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, int]:
    """Generate code for unary operation."""
    operator = expr.get("operator")
    operand = expr.get("operand")
    
    # Evaluate operand
    operand_asm, _, offset_after = generate_expression_code(operand, var_offsets, next_offset)
    
    # Generate unary operation code
    if operator == "-":
        op_asm = "RSB R0, R0, #0\n"
    elif operator == "not":
        op_asm = "CMP R0, #0\nMOVEQ R0, #1\nMOVNE R0, #0\n"
    else:
        raise ValueError(f"Unknown unary operator: {operator}")
    
    return operand_asm + op_asm, 0, offset_after

# === OOP compatibility layer ===
# Not needed - this is a pure function node
