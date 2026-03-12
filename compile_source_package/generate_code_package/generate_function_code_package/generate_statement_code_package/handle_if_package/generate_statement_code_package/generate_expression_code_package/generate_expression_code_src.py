# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions - this is a leaf node

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset for variable
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": "LITERAL" | "IDENT" | "BINARY" | "UNARY",
#   "value": int,              # For LITERAL
#   "name": str,               # For IDENT
#   "op": str,                 # For BINARY/UNARY
#   "left": dict,              # For BINARY
#   "right": dict,             # For BINARY
#   "operand": dict,           # For UNARY
# }

ExprResult = Tuple[str, int, str]
# ExprResult possible fields:
# {
#   [0]: str,  # assembly code (4-space indented lines)
#   [1]: int,  # updated next_offset
#   [2]: str,  # result register name (e.g., "x0")
# }

# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> ExprResult:
    """Generate ARM64 assembly code for expression evaluation."""
    expr_type = expr.get("type")
    
    if expr_type == "LITERAL":
        value = expr.get("value", 0)
        code = f"    mov x0, #{value}"
        return (code, next_offset, "x0")
    
    elif expr_type == "IDENT":
        var_name = expr.get("name", "")
        if var_name not in var_offsets:
            raise KeyError(f"Undefined variable: {var_name}")
        offset = var_offsets[var_name]
        code = f"    ldr x0, [sp, #{offset * 8}]"
        return (code, next_offset, "x0")
    
    elif expr_type == "BINARY":
        return _handle_binary(expr, var_offsets, next_offset)
    
    elif expr_type == "UNARY":
        return _handle_unary(expr, var_offsets, next_offset)
    
    else:
        raise ValueError(f"Unsupported expression type: {expr_type}")

# === helper functions ===
def _handle_binary(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> ExprResult:
    """Handle BINARY expression types."""
    op = expr.get("op", "")
    left_expr = expr.get("left", {})
    right_expr = expr.get("right", {})
    
    # Evaluate left operand (result in x0)
    left_code, next_offset, left_reg = generate_expression_code(left_expr, var_offsets, next_offset)
    
    # Evaluate right operand (result in x0, we'll need to manage registers)
    right_code, next_offset, right_reg = generate_expression_code(right_expr, var_offsets, next_offset)
    
    # Build instruction based on operator
    lines = [left_code, right_code]
    
    if op in ("==", "!=", "<", ">", "<=", ">="):
        # Comparison: cmp + cset
        cmp_map = {
            "==": "eq", "!=": "ne", "<": "lt",
            ">": "gt", "<=": "le", ">=": "ge"
        }
        cond = cmp_map[op]
        lines.append(f"    cmp x0, x1")
        lines.append(f"    cset x0, {cond}")
    elif op == "+":
        lines.append(f"    add x0, x0, x1")
    elif op == "-":
        lines.append(f"    sub x0, x0, x1")
    elif op == "*":
        lines.append(f"    mul x0, x0, x1")
    elif op == "/":
        lines.append(f"    udiv x0, x0, x1")
    else:
        raise ValueError(f"Unsupported binary operator: {op}")
    
    code = "\n".join(lines)
    return (code, next_offset, "x0")

def _handle_unary(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> ExprResult:
    """Handle UNARY expression types."""
    op = expr.get("op", "")
    operand_expr = expr.get("operand", {})
    
    # Evaluate operand (result in x0)
    operand_code, next_offset, operand_reg = generate_expression_code(operand_expr, var_offsets, next_offset)
    
    lines = [operand_code]
    
    if op == "neg":
        lines.append(f"    neg x0, x0")
    elif op == "not":
        lines.append(f"    cmp x0, #0")
        lines.append(f"    cset x0, eq")
    else:
        raise ValueError(f"Unsupported unary operator: {op}")
    
    code = "\n".join(lines)
    return (code, next_offset, "x0")

# === OOP compatibility layer ===
# Not needed - this is a pure function node
