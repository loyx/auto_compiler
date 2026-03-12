# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .handle_if_package.handle_if_src import handle_if
from .handle_assign_package.handle_assign_src import handle_assign
from .handle_return_package.handle_return_src import handle_return
from .handle_while_package.handle_while_src import handle_while
from .handle_decl_package.handle_decl_src import handle_decl
from .handle_call_package.handle_call_src import handle_call
from .handle_block_package.handle_block_src import handle_block

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
#   "var_name": int,  # stack offset for variable
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,  # "IF", "ASSIGN", "RETURN", "WHILE", "DECL", "CALL", "BLOCK"
#   "condition": dict,  # for IF/WHILE
#   "then_body": list,  # for IF
#   "else_body": list,  # for IF
#   "var_name": str,  # for ASSIGN/DECL
#   "expression": dict,  # for ASSIGN
#   "var_type": str,  # for DECL
#   "value": dict | None,  # for RETURN
#   "func_name": str,  # for CALL
#   "args": list,  # for CALL
#   "body": list,  # for WHILE
#   "statements": list,  # for BLOCK
# }

# === main function ===
def generate_statement_code(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Dispatcher: route statement types to their specific handlers."""
    stmt_type = stmt.get("type", "")
    
    if stmt_type == "IF":
        return handle_if(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "ASSIGN":
        return handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "RETURN":
        return handle_return(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "WHILE":
        return handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "DECL":
        return handle_decl(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "CALL":
        return handle_call(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "BLOCK":
        return handle_block(stmt, func_name, label_counter, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown statement type: {stmt_type}")

# === helper functions ===
# No helper functions needed - pure dispatcher

# === OOP compatibility layer ===
# Not needed for this function node
