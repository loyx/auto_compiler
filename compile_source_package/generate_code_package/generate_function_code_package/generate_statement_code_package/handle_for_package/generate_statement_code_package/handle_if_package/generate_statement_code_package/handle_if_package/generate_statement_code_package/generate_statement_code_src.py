# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .handle_if_statement_package.handle_if_statement_src import handle_if_statement
from .handle_while_statement_package.handle_while_statement_src import handle_while_statement
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

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
#   "type": str,  # "assignment", "if", "while", "return", "expression"
#   "var_name": str,  # for assignment
#   "value": dict,  # for assignment
#   "condition": dict,  # for if/while
#   "then_body": list,  # for if
#   "else_body": list,  # for if
#   "body": list,  # for while
#   "expression": dict,  # for expression statement
#   "value": dict,  # for return
# }

# === main function ===
def generate_statement_code(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for a single statement."""
    stmt_type = stmt.get("type", "")
    
    if stmt_type == "assignment":
        var_name = stmt["var_name"]
        value_expr = stmt["value"]
        asm = generate_expression_code(value_expr, var_offsets)
        if var_name not in var_offsets:
            var_offsets[var_name] = next_offset
            next_offset += 4
        offset = var_offsets[var_name]
        asm += f"    STR R0, [SP, #{offset}]\n"
        return asm, next_offset
    
    elif stmt_type == "if":
        return handle_if_statement(stmt, func_name, label_counter, var_offsets, next_offset)
    
    elif stmt_type == "while":
        return handle_while_statement(stmt, func_name, label_counter, var_offsets, next_offset)
    
    elif stmt_type == "return":
        value_expr = stmt.get("value")
        if value_expr:
            asm = generate_expression_code(value_expr, var_offsets)
            asm += "    STR R0, [SP, #-4]!\n"
        else:
            asm = ""
        asm += "    LDR PC, [SP], #4\n"
        return asm, next_offset
    
    elif stmt_type == "expression":
        expr = stmt["expression"]
        asm = generate_expression_code(expr, var_offsets)
        return asm, next_offset
    
    else:
        return "", next_offset

# === helper functions ===
# No helper functions - all logic delegated to sub-functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node