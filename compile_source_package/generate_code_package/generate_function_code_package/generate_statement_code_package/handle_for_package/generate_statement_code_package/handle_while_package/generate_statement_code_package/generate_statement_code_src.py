# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .handle_while_package.handle_while_src import handle_while
from .handle_assign_package.handle_assign_src import handle_assign
from .handle_if_package.handle_if_src import handle_if
from .handle_return_package.handle_return_src import handle_return
from .handle_call_package.handle_call_src import handle_call
from .handle_var_decl_package.handle_var_decl_src import handle_var_decl
from .handle_block_package.handle_block_src import handle_block

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_end": int,
#   "if_cond": int,
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
#   "type": "WHILE" | "ASSIGN" | "IF" | "RETURN" | "CALL" | "VAR_DECL" | "BLOCK",
#   "condition": dict (for WHILE/IF),
#   "body": list (for WHILE/IF/BLOCK),
#   "target": str (for ASSIGN),
#   "value": dict (for ASSIGN),
#   "else_body": list (for IF),
#   "function": str (for CALL),
#   "args": list (for CALL),
#   "name": str (for VAR_DECL),
#   "init": dict (for VAR_DECL),
#   "statements": list (for BLOCK)
# }

# === main function ===
def generate_statement_code(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Dispatch to appropriate statement handler based on stmt type."""
    stmt_type = stmt.get("type", "")
    
    if stmt_type == "WHILE":
        return handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "ASSIGN":
        return handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "IF":
        return handle_if(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "RETURN":
        return handle_return(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "CALL":
        return handle_call(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "VAR_DECL":
        return handle_var_decl(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "BLOCK":
        return handle_block(stmt, func_name, label_counter, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown statement type: {stmt_type}")

# === helper functions ===
# No helper functions needed - this is a pure dispatcher

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a compiler function node
