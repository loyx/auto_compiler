# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# Lazy import for generate_statement_code to avoid circular dependency issues
# Default to None for testing; will be patched by tests or imported on demand
generate_statement_code = None

def _get_generate_statement_code():
    global generate_statement_code
    if generate_statement_code is not None:
        return generate_statement_code
    from .generate_statement_code_package.generate_statement_code_src import generate_statement_code as gsc
    generate_statement_code = gsc
    return gsc

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
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
#   "condition": dict,
#   "body": list,
# }

# === main function ===
def handle_while(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle WHILE statement. Generate condition label, body, and loop back jump."""
    cond_count = label_counter.get("while_cond", 0)
    end_count = label_counter.get("while_end", 0)
    
    cond_label = f"{func_name}_while_cond_{cond_count}"
    end_label = f"{func_name}_while_end_{end_count}"
    
    label_counter["while_cond"] = cond_count + 1
    label_counter["while_end"] = end_count + 1
    
    code_lines = [f"{cond_label}:"]
    
    condition = stmt.get("condition")
    if condition:
        cond_code, next_offset = generate_expression_code(condition, var_offsets, next_offset)
        code_lines.append(cond_code)
    
    code_lines.append(f"cbz x0, {end_label}")
    
    body = stmt.get("body", [])
    generate_statement_code = _get_generate_statement_code()
    for body_stmt in body:
        body_code, next_offset = generate_statement_code(body_stmt, func_name, label_counter, var_offsets, next_offset)
        code_lines.append(body_code)
    
    code_lines.append(f"b {cond_label}")
    code_lines.append(f"{end_label}:")
    
    return "\n".join(code_lines), next_offset

# === helper functions ===

# === OOP compatibility layer ===
