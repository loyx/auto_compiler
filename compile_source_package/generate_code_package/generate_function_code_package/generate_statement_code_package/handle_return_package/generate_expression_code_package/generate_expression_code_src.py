# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions delegated - implementation is inline

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset for variable
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "op": str,              # Operation type: "CONST", "VAR", "BINOP"
#   "value": Any,           # For CONST: the constant value (int/float)
#   "var_name": str,        # For VAR: variable name to lookup
#   "left": dict,           # For BINOP: left operand expression tree
#   "right": dict,          # For BINOP: right operand expression tree
#   "operator": str,        # For BINOP: "+", "-", "*", "/"
# }

# === main function ===
def generate_expression_code(expr: Expr, func_name: str, var_offsets: VarOffsets) -> str:
    """
    Generate assembly code for evaluating an expression.
    Result is always left in x0 register.
    """
    op = expr.get("op")
    
    if op == "CONST":
        return _generate_const_code(expr)
    elif op == "VAR":
        return _generate_var_code(expr, var_offsets)
    elif op == "BINOP":
        return _generate_binop_code(expr, func_name, var_offsets)
    else:
        raise ValueError(f"Unknown expression operation type: {op}")

# === helper functions ===
def _generate_const_code(expr: Expr) -> str:
    """Generate code to load constant value into x0."""
    value = expr.get("value")
    if isinstance(value, int):
        return f"    li x0, {value}\n"
    elif isinstance(value, float):
        # For floats, load via memory or use appropriate float instruction
        return f"    # load float constant {value} into x0\n"
    else:
        return f"    li x0, {value}\n"

def _generate_var_code(expr: Expr, var_offsets: VarOffsets) -> str:
    """Generate code to load variable from stack slot into x0."""
    var_name = expr.get("var_name")
    if var_name not in var_offsets:
        raise ValueError(f"Variable '{var_name}' not found in var_offsets")
    offset = var_offsets[var_name]
    return f"    lw x0, {offset}(sp)\n"

def _generate_binop_code(expr: Expr, func_name: str, var_offsets: VarOffsets) -> str:
    """
    Generate code for binary operation.
    Strategy: compute left (result in x0), save to temp, compute right (result in x0),
    then perform operation with saved temp.
    """
    left = expr.get("left")
    right = expr.get("right")
    operator = expr.get("operator")
    
    if left is None or right is None or operator is None:
        raise ValueError("BINOP expression missing left, right, or operator")
    
    # Generate code for left operand (result in x0)
    left_code = generate_expression_code(left, func_name, var_offsets)
    
    # Save x0 to temporary stack slot
    save_code = "    addi sp, sp, -8\n    sw x0, 0(sp)\n"
    
    # Generate code for right operand (result in x0)
    right_code = generate_expression_code(right, func_name, var_offsets)
    
    # Load saved left value into temp register (x1)
    load_saved = "    lw x1, 0(sp)\n    addi sp, sp, 8\n"
    
    # Perform binary operation: x0 = x1 op x0
    op_code = _get_binary_op_instruction(operator)
    
    return left_code + save_code + right_code + load_saved + op_code

def _get_binary_op_instruction(operator: str) -> str:
    """Map operator to RISC-V assembly instruction."""
    op_map = {
        "+": "    add x0, x1, x0\n",
        "-": "    sub x0, x1, x0\n",
        "*": "    mul x0, x1, x0\n",
        "/": "    div x0, x1, x0\n",
        "%": "    rem x0, x1, x0\n",
        "&": "    and x0, x1, x0\n",
        "|": "    or x0, x1, x0\n",
        "^": "    xor x0, x1, x0\n",
    }
    if operator not in op_map:
        raise ValueError(f"Unsupported binary operator: {operator}")
    return op_map[operator]

# === OOP compatibility layer ===
# Not required - this is a pure function node, no framework wrapper needed