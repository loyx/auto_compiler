# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .handle_while_stmt_package.handle_while_stmt_src import handle_while_stmt
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_end": int,
#   "if_else": int,
#   "if_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,           # "assign", "while", "if", "return", "break", "continue"
#   "target": str,         # for assign
#   "value": dict,         # for assign
#   "condition": dict,     # for while/if
#   "body": list,          # for while/if
#   "else_body": list,     # for if
#   "expression": dict,    # for return
#   "label": str,          # for break/continue - target loop label
# }


# === main function ===
def generate_statement_code(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate assembly code for a single statement."""
    stmt_type = stmt.get("type", "")
    
    if stmt_type == "assign":
        return _handle_assign(stmt, var_offsets, next_offset)
    elif stmt_type == "while":
        return handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "if":
        return _handle_if(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "return":
        return _handle_return(stmt, var_offsets, next_offset)
    elif stmt_type == "break":
        return _handle_break(stmt), next_offset
    elif stmt_type == "continue":
        return _handle_continue(stmt), next_offset
    else:
        return "", next_offset


# === helper functions ===
def _handle_assign(stmt: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle assignment statement."""
    target = stmt.get("target", "")
    value = stmt.get("value", {})
    
    if target not in var_offsets:
        return "", next_offset
    
    code, _, new_offset = generate_expression_code(value, var_offsets, next_offset)
    offset = var_offsets[target]
    code += f"    STORE {offset}\n"
    return code, new_offset


def _handle_if(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle IF statement with optional else."""
    condition = stmt.get("condition", {})
    body = stmt.get("body", [])
    else_body = stmt.get("else_body", [])
    
    # Generate unique labels
    else_label_id = label_counter.get("if_else", 0)
    end_label_id = label_counter.get("if_end", 0)
    label_counter["if_else"] = else_label_id + 1
    label_counter["if_end"] = end_label_id + 1
    
    else_label = f"{func_name}_if_else_{else_label_id}"
    end_label = f"{func_name}_if_end_{end_label_id}"
    
    # Generate condition code
    code, cond_offset, new_offset = generate_expression_code(condition, var_offsets, next_offset)
    code += f"    JUMP_IF_FALSE {cond_offset}, {else_label}\n"
    
    # Generate then body
    for s in body:
        body_code, new_offset = generate_statement_code(s, func_name, label_counter, var_offsets, new_offset)
        code += body_code
    
    if else_body:
        code += f"    JUMP {end_label}\n"
        code += f"{else_label}:\n"
        for s in else_body:
            body_code, new_offset = generate_statement_code(s, func_name, label_counter, var_offsets, new_offset)
            code += body_code
    
    code += f"{end_label}:\n"
    return code, new_offset


def _handle_return(stmt: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle RETURN statement."""
    expression = stmt.get("expression", {})
    
    if not expression:
        return "    RETURN\n", next_offset
    
    code, ret_offset, new_offset = generate_expression_code(expression, var_offsets, next_offset)
    code += f"    RETURN {ret_offset}\n"
    return code, new_offset


def _handle_break(stmt: dict) -> str:
    """Handle BREAK statement."""
    label = stmt.get("label", "loop_end")
    return f"    JUMP {label}\n"


def _handle_continue(stmt: dict) -> str:
    """Handle CONTINUE statement."""
    label = stmt.get("label", "loop_cond")
    return f"    JUMP {label}\n"


# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
