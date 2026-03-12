# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code
from .generate_statement_code_package.generate_statement_code_src import generate_statement_code

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
#   "type": str,
#   "condition": dict,
#   "body": list,
# }

# === main function ===
def handle_while_statement(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly for while loop statement."""
    # Generate unique labels by incrementing counters
    label_counter["while_start"] = label_counter.get("while_start", 0) + 1
    label_counter["while_end"] = label_counter.get("while_end", 0) + 1
    start_label = f"while_start_{func_name}_{label_counter['while_start']}"
    end_label = f"while_end_{func_name}_{label_counter['while_end']}"
    
    # Emit start label
    asm = f"{start_label}:\n"
    
    # Generate condition code and branch to end if false
    asm += generate_expression_code(stmt["condition"], var_offsets)
    asm += "    CMP R0, #0\n"
    asm += f"    BEQ {end_label}\n"
    
    # Generate code for each statement in body
    for body_stmt in stmt["body"]:
        body_asm, next_offset = generate_statement_code(body_stmt, func_name, label_counter, var_offsets, next_offset)
        asm += body_asm
    
    # Branch back to loop start and emit end label
    asm += f"    B {start_label}\n"
    asm += f"{end_label}:\n"
    
    return asm, next_offset

# === helper functions ===

# === OOP compatibility layer ===
