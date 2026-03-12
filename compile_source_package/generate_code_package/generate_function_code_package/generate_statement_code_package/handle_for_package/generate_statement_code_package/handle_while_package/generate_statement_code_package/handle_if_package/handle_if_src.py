# === std / third-party imports ===
from typing import Dict, Any, Tuple

# === sub function imports ===
# only import child functions
from .evaluate_expression_package.evaluate_expression_src import evaluate_expression
from .generate_statement_code_package.generate_statement_code_src import generate_statement_code

# === ADT defines ===
# define the data structures used between parent and child functions
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_end": int,
#   "if_cond": int,
#   "if_else": int,
#   "if_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": "IF",
#   "condition": dict,
#   "body": list,
#   "else_body": list (optional),
# }

# === main function ===
def handle_if(stmt: Stmt, func_name: str, label_counter: LabelCounter, 
              var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """
    Generate ARM32 assembly code for IF/ELSE statement.
    
    Args:
        stmt: IF statement with 'condition' (expr dict), 'body' (list of stmts), 
              optional 'else_body' (list of stmts)
        func_name: Current function name for label naming
        label_counter: Mutable dict; increments 'if_cond', 'if_else', 'if_end' counters
        var_offsets: Variable offset lookup {var_name: stack_offset}
        next_offset: Current next available stack offset
    
    Returns:
        Tuple[assembly_code, updated_offset]
    """
    # Get current label counts and increment them
    if_cond_count = label_counter.get('if_cond', 0)
    if_else_count = label_counter.get('if_else', 0)
    if_end_count = label_counter.get('if_end', 0)
    
    # Increment counters in-place
    label_counter['if_cond'] = if_cond_count + 1
    label_counter['if_else'] = if_else_count + 1
    label_counter['if_end'] = if_end_count + 1
    
    # Generate label names
    cond_label = f"{func_name}_if_cond_{if_cond_count}"
    else_label = f"{func_name}_if_else_{if_else_count}"
    end_label = f"{func_name}_if_end_{if_end_count}"
    
    asm_lines = []
    
    # Add condition label
    asm_lines.append(f"{cond_label}:")
    
    # Evaluate condition expression
    condition = stmt['condition']
    cond_code, next_offset, _ = evaluate_expression(condition, var_offsets, next_offset)
    asm_lines.append(cond_code)
    
    # Compare result with 0
    asm_lines.append("CMP r0, #0")
    
    # Check if there's an else body
    has_else = 'else_body' in stmt and stmt['else_body']
    
    # Branch based on condition result
    jump_target = else_label if has_else else end_label
    asm_lines.append(f"BEQ {jump_target}")
    
    # Generate code for if body statements
    for if_stmt in stmt['body']:
        body_code, next_offset = generate_statement_code(if_stmt, func_name, label_counter, var_offsets, next_offset)
        asm_lines.append(body_code)
    
    # If there's an else body, branch to end after if body
    if has_else:
        asm_lines.append(f"B {end_label}")
        asm_lines.append(f"{else_label}:")
        
        # Generate code for else body statements
        for else_stmt in stmt['else_body']:
            else_code, next_offset = generate_statement_code(else_stmt, func_name, label_counter, var_offsets, next_offset)
            asm_lines.append(else_code)
    
    # Add end label
    asm_lines.append(f"{end_label}:")
    
    # Join all assembly lines
    assembly_code = "\n".join(asm_lines)
    
    return assembly_code, next_offset

# === helper functions ===
# No helper functions needed - all logic is in main function

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node