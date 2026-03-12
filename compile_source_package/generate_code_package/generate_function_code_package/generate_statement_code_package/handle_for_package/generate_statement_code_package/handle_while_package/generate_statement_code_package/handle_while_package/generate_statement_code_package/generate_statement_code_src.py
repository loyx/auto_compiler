# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .evaluate_expression_package.evaluate_expression_src import evaluate_expression

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_end": int,
#   "if_end": int,
#   "if_else": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,  # "ASSIGN", "IF", "WHILE", "RETURN", "EXPR"
#   "var_name": str,  # for ASSIGN
#   "value": dict,  # for ASSIGN
#   "condition": dict,  # for IF/WHILE
#   "then_body": list,  # for IF
#   "else_body": list,  # for IF
#   "body": list,  # for WHILE
#   "expression": dict,  # for RETURN/EXPR
# }


# === main function ===
def generate_statement_code(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM32 assembly for a single statement."""
    stmt_type = stmt.get("type")
    
    if stmt_type == "ASSIGN":
        return _handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "IF":
        return _handle_if(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "WHILE":
        from .handle_while_package.handle_while_src import handle_while
        return handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "RETURN":
        return _handle_return(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "EXPR":
        return _handle_expr(stmt, func_name, label_counter, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown statement type: {stmt_type}")


# === helper functions ===
def _handle_assign(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, offset: int) -> Tuple[str, int]:
    """Handle ASSIGN: evaluate value and store to variable's stack slot."""
    var_name = stmt["var_name"]
    value_expr = stmt["value"]
    
    code_lines = []
    
    # Evaluate value expression (result in r0)
    value_code, offset = evaluate_expression(value_expr, func_name, label_counter, var_offsets, offset)
    code_lines.append(value_code)
    
    # Store to stack
    var_offset = var_offsets[var_name]
    code_lines.append(f"    str r0, [sp, #{var_offset}]")
    
    return "\n".join(code_lines), offset


def _handle_if(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, offset: int) -> Tuple[str, int]:
    """Handle IF: evaluate condition and branch to then/else bodies."""
    condition = stmt["condition"]
    then_body = stmt.get("then_body", [])
    else_body = stmt.get("else_body", [])
    
    code_lines = []
    
    # Evaluate condition (result in r0)
    cond_code, offset = evaluate_expression(condition, func_name, label_counter, var_offsets, offset)
    code_lines.append(cond_code)
    
    # Compare with 0 and branch to else if false
    if_end_counter = label_counter.get("if_end", 0)
    label_counter["if_end"] = if_end_counter + 1
    if_end_label = f"{func_name}_if_end_{if_end_counter}"
    
    has_else = bool(else_body)
    
    if has_else:
        if_else_counter = label_counter.get("if_else", 0)
        label_counter["if_else"] = if_else_counter + 1
        if_else_label = f"{func_name}_if_else_{if_else_counter}"
        code_lines.append("    cmp r0, #0")
        code_lines.append(f"    beq {if_else_label}")
    else:
        code_lines.append("    cmp r0, #0")
        code_lines.append(f"    beq {if_end_label}")
    
    # Generate then_body
    for s in then_body:
        body_code, offset = generate_statement_code(s, func_name, label_counter, var_offsets, offset)
        code_lines.append(body_code)
    
    if has_else:
        code_lines.append(f"    b {if_end_label}")
        code_lines.append(f"{if_else_label}:")
        for s in else_body:
            body_code, offset = generate_statement_code(s, func_name, label_counter, var_offsets, offset)
            code_lines.append(body_code)
    
    code_lines.append(f"{if_end_label}:")
    
    return "\n".join(code_lines), offset


def _handle_return(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, offset: int) -> Tuple[str, int]:
    """Handle RETURN: evaluate expression (if present) and return."""
    code_lines = []
    
    expression = stmt.get("expression")
    if expression is not None:
        expr_code, offset = evaluate_expression(expression, func_name, label_counter, var_offsets, offset)
        code_lines.append(expr_code)
    
    code_lines.append("    bx lr")
    
    return "\n".join(code_lines), offset


def _handle_expr(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, offset: int) -> Tuple[str, int]:
    """Handle EXPR: evaluate expression (result discarded)."""
    expression = stmt["expression"]
    
    code, offset = evaluate_expression(expression, func_name, label_counter, var_offsets, offset)
    return code, offset

# === OOP compatibility layer ===
