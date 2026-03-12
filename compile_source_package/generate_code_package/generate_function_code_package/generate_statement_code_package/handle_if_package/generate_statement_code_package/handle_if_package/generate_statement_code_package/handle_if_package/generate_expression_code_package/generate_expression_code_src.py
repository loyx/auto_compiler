# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions - this is a recursive function that calls itself

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,          # e.g., "BINARY", "UNARY", "LITERAL", "VARIABLE"
#   "operator": str,      # for BINARY/UNARY: e.g., "+", "-", "*", "/", "==", "!="
#   "left": dict,         # for BINARY: left operand expression dict
#   "right": dict,        # for BINARY: right operand expression dict
#   "operand": dict,      # for UNARY: operand expression dict
#   "value": Any,         # for LITERAL: the literal value
#   "name": str,          # for VARIABLE: variable name
# }

# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, int]:
    """
    Generate assembly code for an expression tree.
    Returns: (assembly_code, result_stack_offset, updated_next_offset)
    """
    expr_type = expr["type"]
    
    if expr_type == "LITERAL":
        value = expr["value"]
        result_offset = next_offset
        code = f"    LOAD_CONST {value}\n    STORE {result_offset}\n"
        return code, result_offset, next_offset + 1
    
    elif expr_type == "VARIABLE":
        name = expr["name"]
        if name not in var_offsets:
            raise ValueError(f"Undefined variable: {name}")
        var_offset = var_offsets[name]
        result_offset = next_offset
        code = f"    LOAD {var_offset}\n    STORE {result_offset}\n"
        return code, result_offset, next_offset + 1
    
    elif expr_type == "BINARY":
        left_expr = expr["left"]
        right_expr = expr["right"]
        operator = expr["operator"]
        
        # Generate code for left operand
        left_code, left_offset, next_offset = generate_expression_code(left_expr, var_offsets, next_offset)
        
        # Generate code for right operand
        right_code, right_offset, next_offset = generate_expression_code(right_expr, var_offsets, next_offset)
        
        # Emit binary operation
        result_offset = next_offset
        op_instruction = _binary_op_to_instruction(operator)
        bin_code = f"    LOAD {left_offset}\n    LOAD {right_offset}\n    {op_instruction}\n    STORE {result_offset}\n"
        
        return left_code + right_code + bin_code, result_offset, next_offset + 1
    
    elif expr_type == "UNARY":
        operand_expr = expr["operand"]
        operator = expr["operator"]
        
        # Generate code for operand
        operand_code, operand_offset, next_offset = generate_expression_code(operand_expr, var_offsets, next_offset)
        
        # Emit unary operation
        result_offset = next_offset
        op_instruction = _unary_op_to_instruction(operator)
        unary_code = f"    LOAD {operand_offset}\n    {op_instruction}\n    STORE {result_offset}\n"
        
        return operand_code + unary_code, result_offset, next_offset + 1
    
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
def _binary_op_to_instruction(operator: str) -> str:
    """Map binary operator to assembly instruction."""
    op_map = {
        "+": "ADD",
        "-": "SUB",
        "*": "MUL",
        "/": "DIV",
        "==": "EQ",
        "!=": "NE",
        "<": "LT",
        "<=": "LE",
        ">": "GT",
        ">=": "GE",
    }
    if operator not in op_map:
        raise ValueError(f"Unknown binary operator: {operator}")
    return op_map[operator]

def _unary_op_to_instruction(operator: str) -> str:
    """Map unary operator to assembly instruction."""
    op_map = {
        "-": "NEG",
        "not": "NOT",
    }
    if operator not in op_map:
        raise ValueError(f"Unknown unary operator: {operator}")
    return op_map[operator]

# === OOP compatibility layer ===
# Not needed for this function node