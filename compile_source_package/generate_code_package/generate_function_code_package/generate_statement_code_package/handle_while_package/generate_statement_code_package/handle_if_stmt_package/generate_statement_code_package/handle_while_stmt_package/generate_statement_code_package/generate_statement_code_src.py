# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .handle_while_stmt_package.handle_while_stmt_src import handle_while_stmt
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_end": int,
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
#   "type": str,
#   "condition": dict,
#   "body": list,
#   "then_body": list,
#   "else_body": list,
#   "target": str,
#   "value": dict,
#   "expression": dict,
#   "name": str,
#   "init_value": dict,
# }

# === main function ===
def generate_statement_code(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM64 assembly code for a single statement."""
    code_lines = []
    stmt_type = stmt["type"]
    
    if stmt_type == "while":
        return handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
    
    elif stmt_type == "if":
        condition = stmt["condition"]
        then_body = stmt.get("then_body", [])
        else_body = stmt.get("else_body", [])
        
        else_label = f"{func_name}_if_else_{label_counter['if_else']}"
        label_counter['if_else'] += 1
        end_label = f"{func_name}_if_end_{label_counter['if_end']}"
        label_counter['if_end'] += 1
        
        cond_code, next_offset = generate_expression_code(condition, var_offsets, next_offset)
        code_lines.append(cond_code)
        code_lines.append(f"cbz x0, {else_label}")
        
        for then_stmt in then_body:
            body_code, next_offset = generate_statement_code(then_stmt, func_name, label_counter, var_offsets, next_offset)
            code_lines.append(body_code)
        
        if else_body:
            code_lines.append(f"b {end_label}")
        
        code_lines.append(f"{else_label}:")
        for else_stmt in else_body:
            body_code, next_offset = generate_statement_code(else_stmt, func_name, label_counter, var_offsets, next_offset)
            code_lines.append(body_code)
        
        code_lines.append(f"{end_label}:")
    
    elif stmt_type == "assignment":
        target = stmt["target"]
        value = stmt["value"]
        
        value_code, next_offset = generate_expression_code(value, var_offsets, next_offset)
        code_lines.append(value_code)
        
        offset = var_offsets[target]
        code_lines.append(f"str x0, [sp, #{offset}]")
    
    elif stmt_type == "return":
        value = stmt.get("value")
        if value is not None:
            value_code, next_offset = generate_expression_code(value, var_offsets, next_offset)
            code_lines.append(value_code)
        code_lines.append("ret")
    
    elif stmt_type == "expr_stmt":
        expression = stmt["expression"]
        expr_code, next_offset = generate_expression_code(expression, var_offsets, next_offset)
        code_lines.append(expr_code)
    
    elif stmt_type == "var_decl":
        name = stmt["name"]
        init_value = stmt.get("init_value")
        
        if init_value is not None:
            value_code, next_offset = generate_expression_code(init_value, var_offsets, next_offset)
            code_lines.append(value_code)
            offset = var_offsets[name]
            code_lines.append(f"str x0, [sp, #{offset}]")
    
    code = "\n".join(code_lines) + "\n"
    return (code, next_offset)

# === helper functions ===

# === OOP compatibility layer ===
