# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code
from .generate_statement_code_package.generate_statement_code_src import generate_statement_code

# === ADT defines ===
LabelCounter = Dict[str, Any]
# LabelCounter possible fields:
# {
#   "while_start": int,
#   "while_end": int,
#   "if_else": int,
#   "if_end": int,
#   "loop_stack": list,
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
#   "name": str,
#   "init_value": dict,
#   "value": dict,
#   "condition": dict,
#   "body": list,
#   "else_body": list,
# }

# === main function ===
def handle_while(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle WHILE statement code generation."""
    # Get and increment label counters
    start_count = label_counter["while_start"]
    end_count = label_counter["while_end"]
    label_counter["while_start"] += 1
    label_counter["while_end"] += 1
    
    # Generate label names
    while_start_label = f"{func_name}_while_start_{start_count}"
    while_end_label = f"{func_name}_while_end_{end_count}"
    
    # Push end label onto loop_stack for BREAK support
    label_counter["loop_stack"].append(while_end_label)
    
    # Build assembly code
    code_lines = []
    
    # While start label (no indentation)
    code_lines.append(f"{while_start_label}:")
    
    # Generate condition code
    condition = stmt.get("condition", {})
    cond_code, cond_reg, next_offset = generate_expression_code(condition, var_offsets, next_offset)
    code_lines.append(_indent(cond_code))
    
    # Jump to end if condition is false (zero)
    code_lines.append(f"    cbz x{cond_reg}, {while_end_label}")
    
    # Process body statements
    body = stmt.get("body", [])
    for body_stmt in body:
        body_code, next_offset = generate_statement_code(body_stmt, func_name, label_counter, var_offsets, next_offset)
        code_lines.append(_indent(body_code))
    
    # Jump back to start
    code_lines.append(f"    b {while_start_label}")
    
    # While end label (no indentation)
    code_lines.append(f"{while_end_label}:")
    
    # Pop from loop_stack
    label_counter["loop_stack"].pop()
    
    assembly_code = "\n".join(code_lines)
    return (assembly_code, next_offset)

# === helper functions ===
def _indent(code: str) -> str:
    """Indent all non-empty lines by 4 spaces."""
    lines = code.split("\n")
    indented = []
    for line in lines:
        if line.strip():
            indented.append("    " + line)
        else:
            indented.append(line)
    return "\n".join(indented)

# === OOP compatibility layer ===
