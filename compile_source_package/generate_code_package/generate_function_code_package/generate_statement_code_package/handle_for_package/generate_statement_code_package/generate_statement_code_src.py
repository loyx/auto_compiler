# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .handle_for_package.handle_for_src import handle_for
from .handle_if_package.handle_if_src import handle_if
from .handle_while_package.handle_while_src import handle_while
from .handle_return_package.handle_return_src import handle_return
from .handle_assign_package.handle_assign_src import handle_assign
from .handle_block_package.handle_block_src import handle_block
from .handle_decl_package.handle_decl_src import handle_decl
from .handle_call_package.handle_call_src import handle_call
from .handle_break_package.handle_break_src import handle_break
from .handle_continue_package.handle_continue_src import handle_continue

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
#   "if_else": int,
#   "if_end": int,
#   "while_cond": int,
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
#   "type": str,  # e.g., "FOR", "IF", "WHILE", "RETURN", "ASSIGN", etc.
#   ... type-specific fields
# }

# === main function ===
def generate_statement_code(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Dispatch statement type to appropriate handler and return generated ARM assembly code."""
    stmt_type = stmt.get("type", "UNKNOWN")
    
    handler = HANDLERS.get(stmt_type)
    if handler is None:
        raise ValueError(f"Unsupported statement type: {stmt_type}")
    
    return handler(stmt, func_name, label_counter, var_offsets, next_offset)

# === helper functions ===
HANDLERS = {
    "FOR": handle_for,
    "IF": handle_if,
    "WHILE": handle_while,
    "RETURN": handle_return,
    "ASSIGN": handle_assign,
    "BLOCK": handle_block,
    "DECL": handle_decl,
    "CALL": handle_call,
    "BREAK": handle_break,
    "CONTINUE": handle_continue,
}

# === OOP compatibility layer ===
