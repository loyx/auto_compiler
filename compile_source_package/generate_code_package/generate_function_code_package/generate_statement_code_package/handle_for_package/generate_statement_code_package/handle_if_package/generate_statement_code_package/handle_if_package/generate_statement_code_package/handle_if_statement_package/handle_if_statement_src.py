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
#   "then_body": list,
#   "else_body": list,
# }

# === main function ===
def handle_if_statement(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly for if-else statement."""
    # Generate unique labels using current counter values
    else_label_num = label_counter.get("if_else", 0)
    end_label_num = label_counter.get("if_end", 0)
    label_counter["if_else"] = else_label_num + 1
    label_counter["if_end"] = end_label_num + 1
    
    else_label = f"{func_name}_else_{else_label_num}"
    end_label = f"{func_name}_endif_{end_label_num}"
    
    # Generate condition code
    condition = stmt["condition"]
    asm_condition = generate_expression_code(condition, var_offsets)
    
    # Check if else body exists
    has_else = stmt.get("else_body") is not None
    branch_label = else_label if has_else else end_label
    
    # Build assembly: condition check + branch
    asm = asm_condition
    asm += f"    CMP R0, #0\n"
    asm += f"    BEQ {branch_label}\n"
    
    # Process then_body statements
    current_offset = next_offset
    for then_stmt in stmt["then_body"]:
        asm_body, current_offset = generate_statement_code(
            then_stmt, func_name, label_counter, var_offsets, current_offset
        )
        asm += asm_body
    
    # Handle else branch if present
    if has_else:
        # Jump to end after then_body completes
        asm += f"    B {end_label}\n"
        # Emit else label
        asm += f"{else_label}:\n"
        # Process else_body statements
        for else_stmt in stmt["else_body"]:
            asm_else, current_offset = generate_statement_code(
                else_stmt, func_name, label_counter, var_offsets, current_offset
            )
            asm += asm_else
    
    # Emit end label
    asm += f"{end_label}:\n"
    
    return (asm, current_offset)

# === helper functions ===
# No helper functions needed; all logic is in main function

# === OOP compatibility layer ===
# No OOP wrapper needed; this is a plain function node
