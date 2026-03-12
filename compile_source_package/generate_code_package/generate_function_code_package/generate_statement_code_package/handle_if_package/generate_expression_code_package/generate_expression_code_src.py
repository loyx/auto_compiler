# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": "BINARY" | "UNARY" | "LITERAL" | "IDENT",
#   "operator": str,
#   "left": dict,
#   "right": dict,
#   "operand": dict,
#   "value": int,
#   "name": str,
# }

# === main function ===
def generate_expression_code(expr: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, str]:
    """Generate ARM64 assembly code for expression evaluation."""
    expr_type = expr.get("type")
    
    if expr_type == "LITERAL":
        return _gen_literal(expr, next_offset)
    elif expr_type == "IDENT":
        return _gen_ident(expr, var_offsets, next_offset)
    elif expr_type == "BINARY":
        return _gen_binary(expr, var_offsets, next_offset)
    elif expr_type == "UNARY":
        return _gen_unary(expr, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
def _gen_literal(expr: Expr, next_offset: int) -> Tuple[str, int, str]:
    """Generate code for literal value: mov w0, #value"""
    value = expr["value"]
    code = f"    mov w0, #{value}\n"
    return code, next_offset, "w0"

def _gen_ident(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """Generate code for identifier: ldr w0, [sp, #offset]"""
    var_name = expr["name"]
    if var_name not in var_offsets:
        raise KeyError(f"Undefined variable: {var_name}")
    offset = var_offsets[var_name]
    code = f"    ldr w0, [sp, #{offset}]\n"
    return code, next_offset, "w0"

def _gen_binary(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """Generate code for binary operation."""
    op = expr["operator"]
    left_expr = expr["left"]
    right_expr = expr["right"]
    
    # Evaluate left operand (result in some register)
    left_code, next_offset, left_reg = generate_expression_code(left_expr, var_offsets, next_offset)
    
    # Evaluate right operand (result in some register)
    right_code, next_offset, right_reg = generate_expression_code(right_expr, var_offsets, next_offset)
    
    # Determine result register and generate operation
    result_reg = "w0"
    
    if op in ("+", "-", "*", "/", "&", "|", "^"):
        # Arithmetic/bitwise: result = left op right
        instr_map = {
            "+": "add", "-": "sub", "*": "mul", "/": "sdiv",
            "&": "and", "|": "orr", "^": "eor"
        }
        instr = instr_map[op]
        code = left_code + right_code
        code += f"    {instr} {result_reg}, {left_reg}, {right_reg}\n"
    elif op in ("==", "!=", "<", "<=", ">", ">="):
        # Comparison: cmp then cset
        cond_map = {
            "==": "eq", "!=": "ne", "<": "lt", "<=": "le", ">": "gt", ">=": "ge"
        }
        cond = cond_map[op]
        code = left_code + right_code
        code += f"    cmp {left_reg}, {right_reg}\n"
        code += f"    cset {result_reg}, {cond}\n"
    elif op in ("&&", "||"):
        # Logical: and/orr (operands assumed 0/1)
        instr = "and" if op == "&&" else "orr"
        code = left_code + right_code
        code += f"    {instr} {result_reg}, {left_reg}, {right_reg}\n"
    else:
        raise ValueError(f"Unknown binary operator: {op}")
    
    return code, next_offset, result_reg

def _gen_unary(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """Generate code for unary operation."""
    op = expr["operator"]
    operand_expr = expr["operand"]
    
    # Evaluate operand
    operand_code, next_offset, operand_reg = generate_expression_code(operand_expr, var_offsets, next_offset)
    
    result_reg = "w0"
    
    if op == "-":
        # Negation: neg w0, wn
        code = operand_code
        code += f"    neg {result_reg}, {operand_reg}\n"
    elif op == "!":
        # Logical not: cmp wn, #0; cset w0, eq
        code = operand_code
        code += f"    cmp {operand_reg}, #0\n"
        code += f"    cset {result_reg}, eq\n"
    elif op == "~":
        # Bitwise not: mvn w0, wn
        code = operand_code
        code += f"    mvn {result_reg}, {operand_reg}\n"
    else:
        raise ValueError(f"Unknown unary operator: {op}")
    
    return code, next_offset, result_reg

# === OOP compatibility layer ===
