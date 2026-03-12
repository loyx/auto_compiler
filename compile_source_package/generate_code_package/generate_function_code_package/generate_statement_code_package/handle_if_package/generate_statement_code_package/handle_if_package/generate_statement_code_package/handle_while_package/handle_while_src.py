# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code
from .generate_statement_code_package.generate_statement_code_src import generate_statement_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_start": int,
#   "while_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields for WHILE:
# {
#   "type": "WHILE",
#   "condition": dict,      # Expression dict
#   "body": list,           # List of statement dicts
# }

# === main function ===
def handle_while(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """
    Handle WHILE statement code generation.
    
    Generates assembly code for a while loop with proper labels and jumps.
    Updates label_counter in-place for used labels.
    """
    # Extract while statement components
    condition = stmt["condition"]
    body = stmt["body"]
    
    # Get current counter values and increment them
    start_count = label_counter.get("while_start", 0)
    end_count = label_counter.get("while_end", 0)
    
    # Generate unique label names
    start_label = f"{func_name}_while_start_{start_count}"
    end_label = f"{func_name}_while_end_{end_count}"
    
    # Update label counters in-place
    label_counter["while_start"] = start_count + 1
    label_counter["while_end"] = end_count + 1
    
    # Build assembly code
    code_lines = []
    
    # Emit start label (unindented)
    code_lines.append(f"{start_label}:")
    
    # Generate condition expression code
    cond_code, next_offset = generate_expression_code(condition, var_offsets, next_offset)
    if cond_code:
        code_lines.append(cond_code)
    
    # Emit JZ instruction to jump to end label if condition is false
    code_lines.append(f"    JZ {end_label}")
    
    # Process body statements
    for body_stmt in body:
        body_code, next_offset = generate_statement_code(body_stmt, func_name, label_counter, var_offsets, next_offset)
        if body_code:
            code_lines.append(body_code)
    
    # Emit unconditional jump back to start label
    code_lines.append(f"    B {start_label}")
    
    # Emit end label (unindented)
    code_lines.append(f"{end_label}:")
    
    # Join all code lines
    assembly_code = "\n".join(code_lines)
    
    return assembly_code, next_offset

# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# Not required for this function node