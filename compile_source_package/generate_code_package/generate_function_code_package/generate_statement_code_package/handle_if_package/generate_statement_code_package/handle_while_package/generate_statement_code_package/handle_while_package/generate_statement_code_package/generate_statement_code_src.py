# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .handle_let_package.handle_let_src import handle_let
from .handle_if_package.handle_if_src import handle_if
from .handle_while_package.handle_while_src import handle_while
from .handle_break_package.handle_break_src import handle_break
from .handle_continue_package.handle_continue_src import handle_continue
from .handle_return_package.handle_return_src import handle_return
from .handle_assignment_package.handle_assignment_src import handle_assignment

# === ADT defines ===
LabelCounter = Dict[str, Any]
# LabelCounter possible fields:
# {
#   "while_start": int,
#   "while_end": int,
#   "if_else": int,
#   "if_end": int,
#   "loop_stack": list,  # list of {"start": str, "end": str} dicts
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name -> stack offset
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,  # "LET", "IF", "WHILE", "BREAK", "CONTINUE", "RETURN", "ASSIGN"
#   "name": str,  # for LET statements (variable name)
#   "init_value": dict,  # for LET statements (expression dict)
#   "value": dict,  # for assignment/return statements (expression dict)
#   "condition": dict,  # for IF and WHILE statements (expression dict)
#   "body": list,  # for IF and WHILE statements (list of stmt dicts)
#   "else_body": list,  # for IF statements (list of stmt dicts)
# }

# === main function ===
def generate_statement_code(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate assembly code for a single statement by dispatching to type-specific handlers."""
    stmt_type = stmt.get("type", "")
    
    if stmt_type == "LET":
        return handle_let(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "IF":
        return handle_if(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "WHILE":
        return handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "BREAK":
        code = handle_break(func_name, label_counter)
        return (code, next_offset)
    elif stmt_type == "CONTINUE":
        code = handle_continue(func_name, label_counter)
        return (code, next_offset)
    elif stmt_type == "RETURN":
        return handle_return(stmt, var_offsets, next_offset)
    elif stmt_type in ("ASSIGN", "SET"):
        return handle_assignment(stmt, func_name, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown statement type: {stmt_type}")

# === helper functions ===
# No helper functions needed - all logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed for this function node