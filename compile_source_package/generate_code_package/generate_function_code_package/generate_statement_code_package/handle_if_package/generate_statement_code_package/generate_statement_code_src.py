# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .handle_if_package.handle_if_src import handle_if
from .handle_assign_package.handle_assign_src import handle_assign
from .handle_return_package.handle_return_src import handle_return
from .handle_while_package.handle_while_src import handle_while

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
#   "type": "IF" | "ASSIGN" | "RETURN" | "WHILE" | "BREAK" | "CONTINUE" | "DECL" | "EXPR" | "BLOCK",
#   "condition": dict,         # For IF/WHILE
#   "then_body": list,         # For IF
#   "else_body": list,         # For IF (optional)
#   "body": list,              # For WHILE
#   "target": str,             # For ASSIGN: variable name
#   "value": dict,             # For ASSIGN: expression dict
#   "expression": dict,        # For RETURN
# }

# === main function ===
def generate_statement_code(stmt: Stmt, func_name: str, label_counter: LabelCounter, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Dispatch statement type to appropriate handler and return assembly code."""
    stmt_type = stmt.get("type")
    
    if stmt_type == "IF":
        return handle_if(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "ASSIGN":
        return handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "RETURN":
        return handle_return(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "WHILE":
        return handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
    elif stmt_type == "BREAK":
        return _handle_break(stmt, func_name, next_offset)
    elif stmt_type == "CONTINUE":
        return _handle_continue(stmt, func_name, next_offset)
    elif stmt_type == "DECL":
        return _handle_decl(stmt, var_offsets, next_offset)
    elif stmt_type == "EXPR":
        return _handle_expr_stmt(stmt, var_offsets, next_offset)
    elif stmt_type == "BLOCK":
        return _handle_block(stmt, func_name, label_counter, var_offsets, next_offset)
    else:
        raise ValueError(f"Unsupported statement type: {stmt_type}")

# === helper functions ===
def _handle_break(stmt: Stmt, func_name: str, next_offset: int) -> Tuple[str, int]:
    """Handle BREAK statement - emit break instruction."""
    code = "    b {func_name}_break_label".format(func_name=func_name)
    return (code, next_offset)

def _handle_continue(stmt: Stmt, func_name: str, next_offset: int) -> Tuple[str, int]:
    """Handle CONTINUE statement - emit continue instruction."""
    code = "    b {func_name}_continue_label".format(func_name=func_name)
    return (code, next_offset)

def _handle_decl(stmt: Stmt, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Handle DECL statement - allocate stack slot for declared variable."""
    var_name = stmt.get("name", "")
    if var_name not in var_offsets:
        var_offsets[var_name] = next_offset
        next_offset += 1
    code = "    ; decl {var_name} at offset {offset}".format(var_name=var_name, offset=var_offsets[var_name])
    return (code, next_offset)

def _handle_expr_stmt(stmt: Stmt, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Handle EXPR statement - evaluate expression and discard result."""
    from .generate_expression_code_package.generate_expression_code_src import generate_expression_code
    expr = stmt.get("expression", {})
    code, next_offset, _ = generate_expression_code(expr, var_offsets, next_offset)
    return (code, next_offset)

def _handle_block(stmt: Stmt, func_name: str, label_counter: LabelCounter, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Handle BLOCK statement - process all statements in the block."""
    statements = stmt.get("statements", [])
    codes = []
    for s in statements:
        code, next_offset = generate_statement_code(s, func_name, label_counter, var_offsets, next_offset)
        codes.append(code)
    return ("\n".join(codes), next_offset)

# === OOP compatibility layer ===
