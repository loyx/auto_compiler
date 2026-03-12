# === std / third-party imports ===
from typing import Any, Dict, List, Tuple

# === sub function imports ===
from .handle_while_stmt_package.handle_while_stmt_src import handle_while_stmt
from .handle_assign_stmt_package.handle_assign_stmt_src import handle_assign_stmt
from .handle_if_stmt_package.handle_if_stmt_src import handle_if_stmt
from .handle_return_stmt_package.handle_return_stmt_src import handle_return_stmt
from .handle_break_stmt_package.handle_break_stmt_src import handle_break_stmt
from .handle_continue_stmt_package.handle_continue_stmt_src import handle_continue_stmt
from .handle_expr_stmt_package.handle_expr_stmt_src import handle_expr_stmt

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_body": int,
#   "while_end": int,
#   "if_cond": int,
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
#   "type": str,           # "assign", "while", "if", "return", "break", "continue", "expr_stmt"
#   "target": str,         # for "assign" type
#   "value": dict,         # for "assign", "return" types
#   "condition": dict,     # for "while", "if" types
#   "body": list,          # for "while", "if" types
#   "expression": dict,    # for "return", "expr_stmt" types
#   "else_body": list,     # for "if" type with else
# }

LoopContext = List[Dict[str, str]]
# LoopContext possible fields:
# [
#   {
#     "break_label": str,
#     "continue_label": str,
#   },
# ]

# === main function ===
def generate_statement_code(stmt: Stmt, func_name: str, label_counter: LabelCounter,
                            var_offsets: VarOffsets, next_offset: int,
                            loop_context: LoopContext = None) -> Tuple[str, int]:
    """Generate assembly code for a statement node by dispatching to handlers."""
    if loop_context is None:
        loop_context = []
    
    stmt_type = stmt.get("type", "")
    
    if stmt_type == "assign":
        return handle_assign_stmt(stmt, var_offsets, next_offset)
    elif stmt_type == "while":
        return handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset, loop_context)
    elif stmt_type == "if":
        return handle_if_stmt(stmt, func_name, label_counter, var_offsets, next_offset, loop_context)
    elif stmt_type == "return":
        return handle_return_stmt(stmt, var_offsets, next_offset)
    elif stmt_type == "break":
        return handle_break_stmt(loop_context)
    elif stmt_type == "continue":
        return handle_continue_stmt(loop_context)
    elif stmt_type == "expr_stmt":
        return handle_expr_stmt(stmt, var_offsets, next_offset)
    else:
        return "", next_offset
