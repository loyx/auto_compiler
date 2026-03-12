# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No sub functions - recursive implementation is inline

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name -> stack offset
# }

Expr = Dict[str, Any]
# Expr possible fields (various expression types):
# {
#   "type": "CONST|VAR|BINOP|UNOP|CALL",
#   "value": any,           # for CONST
#   "var_name": str,        # for VAR
#   "op": str,              # for BINOP/UNOP
#   "left": dict,           # for BINOP
#   "right": dict,          # for BINOP
#   "operand": dict,        # for UNOP
#   "func_name": str,       # for CALL
#   "args": list,           # for CALL
# }

# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """Generate assembly code for an expression tree."""
    expr_type = expr.get("type")
    
    if expr_type == "CONST":
        return _handle_const(expr, next_offset)
    elif expr_type == "VAR":
        return _handle_var(expr, var_offsets, next_offset)
    elif expr_type == "BINOP":
        return _handle_binop(expr, var_offsets, next_offset)
    elif expr_type == "UNOP":
        return _handle_unop(expr, var_offsets, next_offset)
    elif expr_type == "CALL":
        return _handle_call(expr, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
def _handle_const(expr: Expr, next_offset: int) -> Tuple[str, int, str]:
    """Handle constant expression: emit LOAD_CONST."""
    value = expr.get("value")
    result_reg = f"R{next_offset}"
    code = f"    LOAD_CONST {result_reg}, {repr(value)}\n"
    return code, next_offset + 1, result_reg

def _handle_var(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """Handle variable expression: emit LOAD_VAR."""
    var_name = expr.get("var_name")
    if var_name not in var_offsets:
        raise ValueError(f"Undefined variable: {var_name}")
    offset = var_offsets[var_name]
    result_reg = f"R{next_offset}"
    code = f"    LOAD_VAR {result_reg}, [{offset}]\n"
    return code, next_offset + 1, result_reg

def _handle_binop(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """Handle binary operation: generate left, right, then operation."""
    op_map = {
        "+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV",
        "==": "EQ", "!=": "NE", "<": "LT", ">": "GT", "<=": "LE", ">=": "GE",
        "and": "AND", "or": "OR"
    }
    op = expr.get("op")
    if op not in op_map:
        raise ValueError(f"Unknown binary operator: {op}")
    
    left_code, left_offset, left_reg = generate_expression_code(expr["left"], var_offsets, next_offset)
    right_code, right_offset, right_reg = generate_expression_code(expr["right"], var_offsets, left_offset)
    
    result_reg = f"R{right_offset}"
    asm_op = op_map[op]
    op_code = f"    {asm_op} {result_reg}, {left_reg}, {right_reg}\n"
    
    total_code = left_code + right_code + op_code
    return total_code, right_offset + 1, result_reg

def _handle_unop(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """Handle unary operation: generate operand, then operation."""
    op_map = {"-": "NEG", "not": "NOT"}
    op = expr.get("op")
    if op not in op_map:
        raise ValueError(f"Unknown unary operator: {op}")
    
    operand_code, operand_offset, operand_reg = generate_expression_code(expr["operand"], var_offsets, next_offset)
    
    result_reg = f"R{operand_offset}"
    asm_op = op_map[op]
    op_code = f"    {asm_op} {result_reg}, {operand_reg}\n"
    
    total_code = operand_code + op_code
    return total_code, operand_offset + 1, result_reg

def _handle_call(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """Handle function call: generate arg code, then emit CALL."""
    func_name = expr.get("func_name")
    args = expr.get("args", [])
    
    arg_codes = []
    arg_regs = []
    current_offset = next_offset
    
    for arg in args:
        arg_code, current_offset, arg_reg = generate_expression_code(arg, var_offsets, current_offset)
        arg_codes.append(arg_code)
        arg_regs.append(arg_reg)
    
    args_str = ", ".join(arg_regs)
    result_reg = f"R{current_offset}"
    call_code = f"    CALL {result_reg}, {func_name}, {len(args)}, {args_str}\n"
    
    total_code = "".join(arg_codes) + call_code
    return total_code, current_offset + 1, result_reg

# === OOP compatibility layer ===
# Not required - this is a pure function node