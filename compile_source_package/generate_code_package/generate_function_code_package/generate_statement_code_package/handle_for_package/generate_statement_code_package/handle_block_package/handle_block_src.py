# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# Note: generate_statement_code is in the parent module, not a child.
# This is a special case for the statement dispatcher pattern.
# Using lazy import to avoid circular dependency
def _get_generate_statement_code():
    from main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.generate_statement_code_src import generate_statement_code
    return generate_statement_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields for BLOCK:
# {
#   "type": "BLOCK",
#   "statements": list   # 块内语句列表
# }

# === main function ===
def handle_block(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for a BLOCK statement.
    
    Args:
        stmt: Dict with "type"="BLOCK" and "statements" field containing list of child statement dicts
        func_name: Function name for label generation
        label_counter: Mutable dict for label generation (passed to children, may be modified by them)
        var_offsets: Mutable dict for variable offsets (passed to children, may be modified by them)
        next_offset: Starting stack offset
    
    Returns:
        Tuple of (generated_code_string, updated_next_offset)
        - generated_code_string: Concatenated ARM assembly code for all child statements
        - updated_next_offset: Absolute next offset after processing all statements
    """
    code_lines = []
    current_offset = next_offset
    
    statements = stmt.get("statements", [])
    for child_stmt in statements:
        child_code, current_offset = generate_statement_code(
            child_stmt, func_name, label_counter, var_offsets, current_offset
        )
        code_lines.append(child_code)
    
    return "\n".join(code_lines), current_offset

# === helper functions ===
# No helper functions needed for this simple iteration logic

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a function node in the dependency tree
