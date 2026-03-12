# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions - inline implementation

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name mapped to stack offset
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,           # "var", "literal", "binary"
#   "name": str,           # for "var" type: variable name
#   "value": Any,          # for "literal" type: constant value (int|float)
#   "op": str,             # for "binary" type: operator string
#   "left": dict,          # for "binary" type: left operand Expr
#   "right": dict,         # for "binary" type: right operand Expr
# }

# Operator mapping from expression to assembly instruction
OP_MAP = {
    "+": "ADD",
    "-": "SUB",
    "*": "MUL",
    "/": "DIV",
    "<": "LT",
    ">": "GT",
    "<=": "LE",
    ">=": "GE",
    "==": "EQ",
    "!=": "NE",
}

# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, int]:
    """
    Generate assembly code for an expression AST node.
    
    Args:
        expr: Expression dict with "type" field and type-specific fields
        var_offsets: Variable name to stack offset mapping
        next_offset: Current next available stack offset
    
    Returns:
        Tuple of (assembly_code_string, result_stack_offset, updated_next_offset)
    """
    expr_type = expr.get("type")
    
    if expr_type == "literal":
        return _generate_literal_code(expr, next_offset)
    elif expr_type == "var":
        return _generate_var_code(expr, var_offsets, next_offset)
    elif expr_type == "binary":
        return _generate_binary_code(expr, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
def _generate_literal_code(expr: Expr, next_offset: int) -> Tuple[str, int, int]:
    """Generate code for a literal value."""
    value = expr.get("value")
    code = f"PUSH {value}\n"
    result_offset = next_offset
    updated_offset = next_offset + 1
    return (code, result_offset, updated_offset)


def _generate_var_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, int]:
    """Generate code for a variable reference."""
    var_name = expr.get("name")
    if var_name not in var_offsets:
        raise ValueError(f"Undefined variable: {var_name}")
    var_offset = var_offsets[var_name]
    code = f"LOAD {var_offset}\n"
    result_offset = next_offset
    updated_offset = next_offset + 1
    return (code, result_offset, updated_offset)


def _generate_binary_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, int]:
    """Generate code for a binary operation."""
    op = expr.get("op")
    left_expr = expr.get("left")
    right_expr = expr.get("right")
    
    if op not in OP_MAP:
        raise ValueError(f"Unknown operator: {op}")
    
    # Generate left operand code
    left_code, left_offset, offset_after_left = generate_expression_code(
        left_expr, var_offsets, next_offset
    )
    
    # Generate right operand code
    right_code, right_offset, offset_after_right = generate_expression_code(
        right_expr, var_offsets, offset_after_left
    )
    
    # Emit binary operation instruction
    asm_op = OP_MAP[op]
    result_offset = offset_after_right
    updated_offset = offset_after_right + 1
    
    code = left_code + right_code + f"{asm_op}\n"
    return (code, result_offset, updated_offset)

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node
