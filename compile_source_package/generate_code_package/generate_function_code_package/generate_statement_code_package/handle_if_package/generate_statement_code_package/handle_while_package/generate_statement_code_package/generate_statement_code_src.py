# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .handle_while_package.handle_while_src import handle_while
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

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
def generate_statement_code(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate assembly code for a single statement."""
    stmt_type = stmt["type"]
    
    if stmt_type == "DECL":
        return _handle_decl(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "ASSIGN":
        return _handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "IF":
        return _handle_if(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "WHILE":
        return handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "BREAK":
        return _handle_break(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "RETURN":
        return _handle_return(stmt, func_name, label_counter, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown statement type: {stmt_type}")

# === helper functions ===
def _handle_decl(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle DECL statement: register variable and optionally initialize."""
    var_name = stmt["name"]
    var_offsets[var_name] = next_offset
    code_lines = []
    offset = next_offset + 1
    
    if "init_value" in stmt and stmt["init_value"] is not None:
        expr_code, result_reg = generate_expression_code(stmt["init_value"], func_name, var_offsets)
        code_lines.append(expr_code)
        code_lines.append(f"    str {result_reg}, [sp, {next_offset * 8}]")
    
    return "\n".join(code_lines), offset

def _handle_assign(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle ASSIGN statement: evaluate value and store to variable."""
    var_name = stmt["name"]
    offset = var_offsets[var_name]
    expr_code, result_reg = generate_expression_code(stmt["value"], func_name, var_offsets)
    code_lines = [expr_code, f"    str {result_reg}, [sp, {offset * 8}]"]
    return "\n".join(code_lines), next_offset

def _handle_if(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle IF statement: condition, branches, and labels."""
    code_lines = []
    
    # Get and increment counters
    else_count = label_counter.get("if_else", 0)
    end_count = label_counter.get("if_end", 0)
    label_counter["if_else"] = else_count + 1
    label_counter["if_end"] = end_count + 1
    
    else_label = f"{func_name}_if_else_{else_count}"
    end_label = f"{func_name}_if_end_{end_count}"
    
    # Condition code
    cond_code, cond_reg = generate_expression_code(stmt["condition"], func_name, var_offsets)
    code_lines.append(cond_code)
    code_lines.append(f"    cbz {cond_reg}, {else_label}")
    
    # Then body
    for s in stmt.get("body", []):
        body_code, next_offset = generate_statement_code(s, func_name, label_counter, var_offsets, next_offset)
        if body_code:
            code_lines.append(body_code)
    
    if stmt.get("else_body"):
        code_lines.append(f"    b {end_label}")
        code_lines.append(f"{else_label}:")
        for s in stmt["else_body"]:
            body_code, next_offset = generate_statement_code(s, func_name, label_counter, var_offsets, next_offset)
            if body_code:
                code_lines.append(body_code)
        code_lines.append(f"{end_label}:")
    else:
        code_lines.append(f"{else_label}:")
    
    return "\n".join(code_lines), next_offset

def _handle_break(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle BREAK statement: jump to innermost loop end."""
    loop_stack = label_counter.get("loop_stack", [])
    if not loop_stack:
        raise RuntimeError("BREAK outside of loop")
    end_label = loop_stack[-1]
    return f"    b {end_label}", next_offset

def _handle_return(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle RETURN statement: evaluate expression and jump to epilogue."""
    code_lines = []
    epilogue_label = f"{func_name}_epilogue"
    
    if "value" in stmt and stmt["value"] is not None:
        expr_code, result_reg = generate_expression_code(stmt["value"], func_name, var_offsets)
        code_lines.append(expr_code)
        code_lines.append(f"    mov x0, {result_reg}")
    
    code_lines.append(f"    b {epilogue_label}")
    return "\n".join(code_lines), next_offset

# === OOP compatibility layer ===
