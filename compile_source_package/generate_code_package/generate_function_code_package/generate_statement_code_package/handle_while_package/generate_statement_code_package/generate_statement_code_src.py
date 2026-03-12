# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .handle_assign_stmt_package.handle_assign_stmt_src import handle_assign_stmt
from .handle_if_stmt_package.handle_if_stmt_src import handle_if_stmt
from .handle_while_stmt_package.handle_while_stmt_src import handle_while_stmt
from .handle_return_stmt_package.handle_return_stmt_src import handle_return_stmt
from .handle_call_stmt_package.handle_call_stmt_src import handle_call_stmt
from .handle_break_stmt_package.handle_break_stmt_src import handle_break_stmt
from .handle_continue_stmt_package.handle_continue_stmt_src import handle_continue_stmt
from .handle_pass_stmt_package.handle_pass_stmt_src import handle_pass_stmt

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_end": int,
#   "if_else": int,
#   "if_end": int,
#   "break": int,
#   "continue": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,           # ASSIGN, IF, WHILE, RETURN, CALL, BREAK, CONTINUE, PASS
#   "target": str,         # variable name for ASSIGN
#   "value": dict,         # expression for ASSIGN
#   "condition": dict,     # condition for IF/WHILE
#   "then_body": list,     # then body for IF
#   "else_body": list,     # else body for IF (optional)
#   "body": list,          # body statements for WHILE
#   "expression": dict,    # expression for RETURN
#   "function": str,       # function name for CALL
#   "args": list,          # arguments for CALL
# }


# === main function ===
def generate_statement_code(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate assembly code for a statement by dispatching to type-specific handlers."""
    stmt_type = stmt.get("type", "")
    handlers = {
        "ASSIGN": handle_assign_stmt,
        "IF": handle_if_stmt,
        "WHILE": handle_while_stmt,
        "RETURN": handle_return_stmt,
        "CALL": handle_call_stmt,
        "BREAK": handle_break_stmt,
        "CONTINUE": handle_continue_stmt,
        "PASS": handle_pass_stmt,
    }
    handler = handlers.get(stmt_type)
    if handler:
        return handler(stmt, func_name, label_counter, var_offsets, next_offset)
    return "", next_offset
