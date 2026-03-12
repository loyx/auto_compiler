# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code
from .process_statements_package.process_statements_src import process_statements

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
#   "type": str,  # "while", "if", "assign", "return", "expr_stmt"
#   "condition": dict,  # for while/if
#   "body": list,  # for while/if
#   "else_body": list,  # for if
#   "variable": str,  # for assign
#   "value": dict,  # for assign
#   "expression": dict,  # for expr_stmt
#   "return_value": dict,  # for return
# }

# === main function ===
def handle_if_stmt(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly for if-else statement."""
    # Generate unique labels
    if_else_num = label_counter.get("if_else", 0)
    if_end_num = label_counter.get("if_end", 0)
    label_counter["if_else"] = if_else_num + 1
    label_counter["if_end"] = if_end_num + 1
    
    if_else_label = f"{func_name}_if_else_{if_else_num}"
    if_end_label = f"{func_name}_if_end_{if_end_num}"
    
    # Generate condition evaluation code
    condition_asm, offset = generate_expression_code(stmt["condition"], var_offsets, next_offset)
    
    # Build assembly code
    asm_lines = [
        condition_asm,
        f"    CMP R0, #0",
        f"    BEQ {if_else_label}"
    ]
    
    # Process then-body
    body_asm, offset = process_statements(stmt["body"], func_name, label_counter, var_offsets, offset)
    asm_lines.append(body_asm)
    
    # Handle else-body if present
    if "else_body" in stmt and stmt["else_body"]:
        asm_lines.append(f"    B {if_end_label}")
        asm_lines.append(f"{if_else_label}:")
        else_asm, offset = process_statements(stmt["else_body"], func_name, label_counter, var_offsets, offset)
        asm_lines.append(else_asm)
    
    asm_lines.append(f"{if_end_label}:")
    
    return "\n".join(asm_lines), offset

# === helper functions ===
# No helper functions needed - all logic is in main function

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a function node in dependency tree
