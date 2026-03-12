# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .handle_if_package.handle_if_src import handle_if
from .handle_while_package.handle_while_src import handle_while
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

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
#   "var_name": int,  # variable name -> stack offset
# }

Stmt = Dict[str, Any]
# Stmt possible fields (various statement types):
# {
#   "type": "IF|WHILE|FOR|ASSIGN|DECL|RETURN|EXPR|BREAK|CONTINUE|BLOCK",
#   "condition": dict,      # for IF/WHILE
#   "then_body": list,      # for IF
#   "else_body": list,      # for IF (optional)
#   "body": list,           # for WHILE
#   "var_name": str,        # for ASSIGN/DECL
#   "value": dict,          # for ASSIGN/RETURN
#   "initial_value": dict,  # for DECL (optional)
#   "expression": dict,     # for EXPR
#   "statements": list,     # for BLOCK
# }

# === main function ===
def generate_statement_code(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Main dispatcher for all statement types in code generation."""
    stmt_type = stmt.get("type")
    
    if stmt_type == "IF":
        return handle_if(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "WHILE":
        return handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "ASSIGN":
        return _handle_assign(stmt, var_offsets, next_offset)
    elif stmt_type == "DECL":
        return _handle_decl(stmt, var_offsets, next_offset)
    elif stmt_type == "RETURN":
        return _handle_return(stmt, var_offsets, next_offset)
    elif stmt_type == "EXPR":
        return _handle_expr(stmt, var_offsets, next_offset)
    elif stmt_type == "BREAK":
        return ("    BREAK", next_offset)
    elif stmt_type == "CONTINUE":
        return ("    CONTINUE", next_offset)
    elif stmt_type == "BLOCK":
        return _handle_block(stmt, func_name, label_counter, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown statement type: {stmt_type}")

# === helper functions ===
def _handle_assign(stmt: Stmt, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Handle ASSIGN statement: evaluate value expression and store to variable."""
    var_name = stmt["var_name"]
    value_expr = stmt["value"]
    code, next_offset, _ = generate_expression_code(value_expr, var_offsets, next_offset)
    lines = [code] if code else []
    lines.append(f"    STORE_VAR {var_name}")
    return ("\n".join(lines), next_offset)

def _handle_decl(stmt: Stmt, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Handle DECL statement: allocate stack slot and optionally initialize."""
    var_name = stmt["var_name"]
    initial_value = stmt.get("initial_value")
    var_offsets[var_name] = next_offset
    next_offset += 1
    if initial_value:
        code, next_offset, _ = generate_expression_code(initial_value, var_offsets, next_offset)
        lines = [code] if code else []
        lines.append(f"    STORE_VAR {var_name}")
        return ("\n".join(lines), next_offset)
    return ("", next_offset)

def _handle_return(stmt: Stmt, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Handle RETURN statement: optionally evaluate return value and return."""
    value = stmt.get("value")
    if value:
        code, next_offset, _ = generate_expression_code(value, var_offsets, next_offset)
        lines = [code] if code else []
        lines.append("    RET_VALUE")
        return ("\n".join(lines), next_offset)
    return ("    RET", next_offset)

def _handle_expr(stmt: Stmt, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Handle EXPR statement: evaluate expression and discard result."""
    expr = stmt["expression"]
    code, next_offset, _ = generate_expression_code(expr, var_offsets, next_offset)
    return (code, next_offset)

def _handle_block(stmt: Stmt, func_name: str, label_counter: LabelCounter, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Handle BLOCK statement: process each statement in sequence."""
    statements = stmt.get("statements", [])
    all_code = []
    for s in statements:
        code, next_offset = generate_statement_code(s, func_name, label_counter, var_offsets, next_offset)
        if code:
            all_code.append(code)
    return ("\n".join(all_code), next_offset)

# === OOP compatibility layer ===