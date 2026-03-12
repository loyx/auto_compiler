# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .handle_var_decl_package.handle_var_decl_src import handle_var_decl
from .handle_assign_package.handle_assign_src import handle_assign
from .handle_if_package.handle_if_src import handle_if
from .handle_while_package.handle_while_src import handle_while
from .handle_for_package.handle_for_src import handle_for
from .handle_return_package.handle_return_src import handle_return
from .handle_expression_stmt_package.handle_expression_stmt_src import handle_expression_stmt

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "if_else": int,
#   "if_end": int,
#   "while_cond": int,
#   "while_end": int,
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,
#   "var_name": str,
#   "var_type": str,
#   "init_value": dict,
#   "target": str,
#   "value": dict,
#   "condition": dict,
#   "then_body": list,
#   "else_body": list,
#   "init": dict,
#   "update": dict,
#   "body": list,
#   "value": dict,
#   "func_name": str,
#   "args": list,
# }

# === main function ===
def generate_statement_code(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM64 assembly code for a single statement node."""
    stmt_type = stmt.get("type", "")
    
    if stmt_type == "VAR_DECL":
        return handle_var_decl(stmt, func_name, var_offsets, next_offset)
    elif stmt_type == "ASSIGN":
        code = handle_assign(stmt, func_name, var_offsets)
        return code, next_offset
    elif stmt_type == "IF":
        return handle_if(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "WHILE":
        return handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "FOR":
        return handle_for(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "RETURN":
        code = handle_return(stmt, func_name, var_offsets)
        return code, next_offset
    elif stmt_type == "EXPRESSION":
        code = handle_expression_stmt(stmt, func_name, var_offsets)
        return code, next_offset
    elif stmt_type == "BREAK":
        return f"    b {func_name}_break", next_offset
    elif stmt_type == "CONTINUE":
        return f"    // CONTINUE placeholder", next_offset
    else:
        return f"    // Unknown statement type: {stmt_type}", next_offset

# === helper functions ===
# No helper functions - all logic delegated to sub-functions

# === OOP compatibility layer ===
# Not required for this function node
