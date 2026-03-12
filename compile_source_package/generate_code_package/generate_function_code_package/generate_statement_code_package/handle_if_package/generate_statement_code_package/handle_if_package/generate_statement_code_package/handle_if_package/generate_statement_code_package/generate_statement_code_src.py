# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code
from .handle_if_package.handle_if_src import handle_if
from .handle_while_package.handle_while_src import handle_while

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "if_else": int,
#   "if_end": int,
#   "while_start": int,
#   "while_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,          # e.g., "IF", "ASSIGN", "RETURN", "EXPR", "WHILE", "VAR"
#   "target": str,        # for ASSIGN: variable name
#   "value": dict,        # for ASSIGN: expression dict
#   "expression": dict,   # for EXPR: expression dict
#   "condition": dict,    # for IF/WHILE: condition expression dict
#   "then_body": list,    # for IF: list of statement dicts
#   "else_body": list,    # for IF: list of statement dicts (optional)
#   "body": list,         # for WHILE: list of statement dicts
#   "name": str,          # for VAR: variable name
# }


# === main function ===
def generate_statement_code(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate assembly code for a single statement."""
    stmt_type = stmt.get("type", "")
    
    if stmt_type == "IF":
        return handle_if(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "WHILE":
        return handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "ASSIGN":
        return _handle_assign(stmt, var_offsets, next_offset)
    elif stmt_type == "RETURN":
        return _handle_return(stmt, var_offsets, next_offset)
    elif stmt_type == "EXPR":
        return _handle_expr(stmt, var_offsets, next_offset)
    elif stmt_type == "VAR":
        return _handle_var(stmt, var_offsets, next_offset)
    else:
        return "", next_offset


# === helper functions ===
def _handle_assign(stmt: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle ASSIGN statement: generate value code, then STORE to variable offset."""
    target = stmt["target"]
    value_expr = stmt["value"]
    
    # Generate code for the value expression
    value_code, result_offset, next_offset = generate_expression_code(value_expr, var_offsets, next_offset)
    
    # Get the target variable's offset
    target_offset = var_offsets.get(target)
    if target_offset is None:
        raise ValueError(f"Variable '{target}' not declared before assignment")
    
    # Emit STORE instruction
    store_instr = f"    STORE {target_offset}\n"
    
    return value_code + store_instr, next_offset


def _handle_return(stmt: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle RETURN statement: generate return value code (if any), then emit RETURN."""
    return_expr = stmt.get("value")
    
    if return_expr is not None:
        # Generate code for return value expression
        return_code, _, next_offset = generate_expression_code(return_expr, var_offsets, next_offset)
        return_instr = "    RETURN\n"
        return return_code + return_instr, next_offset
    else:
        # No return value
        return "    RETURN\n", next_offset


def _handle_expr(stmt: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle EXPR statement: generate expression code (result left on stack or discarded)."""
    expr = stmt["expression"]
    expr_code, _, next_offset = generate_expression_code(expr, var_offsets, next_offset)
    return expr_code, next_offset


def _handle_var(stmt: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle VAR statement: allocate new variable offset and update var_offsets."""
    var_name = stmt["name"]
    
    if var_name not in var_offsets:
        var_offsets[var_name] = next_offset
        next_offset += 1
    
    return "", next_offset

# === OOP compatibility layer ===
