# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
# No sub function imports needed - all logic inlined

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "name": str,             # 函数名/变量名
#   "params": list,          # 参数列表
#   "return_type": str,      # 返回类型
#   "body": list,            # 函数体/语句体
#   "value": Any,            # 节点值/返回值
# }

LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "if_else": int,
#   "if_end": int,
#   "while_cond": int,
#   "while_end": int,
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
# }

# === main function ===
def generate_code(ast: AST) -> str:
    """将 AST 转换为 ARM64 汇编代码。"""
    if ast.get("type") != "PROGRAM":
        raise ValueError("Root node must be PROGRAM")
    
    lines = []
    label_counter = {"if_else": 0, "if_end": 0, "while_cond": 0, 
                     "while_end": 0, "for_cond": 0, "for_end": 0, "for_update": 0}
    
    # 生成所有函数代码
    for func_def in ast.get("children", []):
        func_code = _generate_function_code(func_def, label_counter)
        lines.append(func_code)
    
    return "\n".join(lines)

def _generate_function_code(func_def: AST, label_counter: LabelCounter) -> str:
    """生成单个函数的汇编代码。"""
    func_name = func_def.get("name", "main")
    params = func_def.get("params", [])
    body = func_def.get("body", [])
    
    lines = []
    lines.append(f".globl {func_name}")
    lines.append(f"{func_name}:")
    lines.append("    stp x29, x30, [sp, -16]!")
    lines.append("    mov x29, sp")
    
    # 分配局部变量空间（简单处理：固定 64 字节）
    lines.append("    sub sp, sp, 64")
    
    # 生成函数体代码
    var_offset = 0
    for stmt in body:
        stmt_code = _generate_statement(stmt, label_counter, var_offset)
        lines.append(stmt_code)
        var_offset += 8
    
    # 如果函数没有 return，添加默认 return 0
    if func_name == "main":
        lines.append("    mov w0, 0")
    
    lines.append("    add sp, sp, 64")
    lines.append("    ldp x29, x30, [sp], 16")
    lines.append("    ret")
    
    return "\n".join(lines)

def _generate_statement(stmt: AST, label_counter: LabelCounter, var_offset: int = 0) -> str:
    """生成语句的汇编代码。"""
    stmt_type = stmt.get("type")
    
    if stmt_type == "VAR_DECL":
        var_name = stmt.get("name")
        init_value = stmt.get("init_value")
        lines = []
        if init_value:
            init_code = _generate_expr(init_value, label_counter)
            lines.append(f"    {init_code}")
            lines.append(f"    str x0, [sp, {var_offset}]")
        return "\n".join(lines)
    
    elif stmt_type == "IF_STMT":
        else_label = f"L_if_else_{label_counter['if_else']}"
        end_label = f"L_if_end_{label_counter['if_end']}"
        label_counter["if_else"] += 1
        label_counter["if_end"] += 1
        
        cond_code = _generate_expr(stmt.get("condition"), label_counter)
        then_code = "\n".join([_generate_statement(s, label_counter, var_offset) for s in stmt.get("then_branch", [])])
        
        lines = []
        lines.append(f"    {cond_code}")
        lines.append("    cmp x0, 0")
        lines.append(f"    beq {else_label}")
        lines.append(then_code)
        
        if stmt.get("else_branch"):
            lines.append(f"    b {end_label}")
            lines.append(f"{else_label}:")
            else_code = "\n".join([_generate_statement(s, label_counter, var_offset) for s in stmt["else_branch"]])
            lines.append(else_code)
            lines.append(f"{end_label}:")
        else:
            lines.append(f"{else_label}:")
        
        return "\n".join(lines)
    
    elif stmt_type == "WHILE_STMT":
        cond_label = f"L_while_cond_{label_counter['while_cond']}"
        end_label = f"L_while_end_{label_counter['while_end']}"
        label_counter["while_cond"] += 1
        label_counter["while_end"] += 1
        
        cond_code = _generate_expr(stmt.get("condition"), label_counter)
        body_code = "\n".join([_generate_statement(s, label_counter, var_offset) for s in stmt.get("body", [])])
        
        lines = []
        lines.append(f"{cond_label}:")
        lines.append(f"    {cond_code}")
        lines.append("    cmp x0, 0")
        lines.append(f"    beq {end_label}")
        lines.append(body_code)
        lines.append(f"    b {cond_label}")
        lines.append(f"{end_label}:")
        
        return "\n".join(lines)
    
    elif stmt_type == "RETURN_STMT":
        value = stmt.get("value")
        if value:
            expr_code = _generate_expr(value, label_counter)
            return f"    {expr_code}\n    mov w0, x0"
        else:
            return "    mov w0, 0"
    
    elif stmt_type == "EXPR_STMT":
        expr = stmt.get("expression")
        if expr.get("type") == "BINARY_OP" and expr.get("operator") == "=":
            return _generate_assignment(expr, label_counter, var_offset)
        else:
            expr_code = _generate_expr(expr, label_counter)
            return f"    {expr_code}"
    
    elif stmt_type == "BREAK_STMT":
        # 简单处理：跳转到循环结束（实际需要更复杂的标签管理）
        return "    b L_while_end_0"
    
    elif stmt_type == "CONTINUE_STMT":
        # 简单处理：跳转到循环条件
        return "    b L_while_cond_0"
    
    return ""

def _generate_assignment(expr: AST, label_counter: LabelCounter, var_offset: int = 0) -> str:
    """生成赋值表达式的汇编代码。"""
    left = expr.get("left")
    right = expr.get("right")
    
    right_code = _generate_expr(right, label_counter)
    
    # 简单处理：假设左边是局部变量
    if left.get("type") == "IDENTIFIER":
        var_name = left.get("name")
        # 这里简化处理，假设所有变量都在栈上
        return f"    {right_code}\n    str x0, [sp, 0]"
    
    return right_code

def _generate_expr(expr: AST, label_counter: LabelCounter) -> str:
    """生成表达式的汇编代码，结果放在 x0 中。"""
    if not expr:
        return "mov x0, 0"
    
    expr_type = expr.get("type")
    
    if expr_type == "LITERAL":
        value = expr.get("value", 0)
        return f"mov x0, {value}"
    
    elif expr_type == "IDENTIFIER":
        var_name = expr.get("name")
        # 简单处理：从栈上加载
        return f"ldr x0, [sp, 0]"
    
    elif expr_type == "BINARY_OP":
        op = expr.get("operator")
        left = expr.get("left")
        right = expr.get("right")
        
        left_code = _generate_expr(left, label_counter)
        right_code = _generate_expr(right, label_counter)
        
        op_map = {
            "+": "add",
            "-": "sub",
            "*": "mul",
            "/": "sdiv",
            "%": "srem",
            "==": "eq",
            "!=": "ne",
            "<": "lt",
            ">": "gt",
            "<=": "le",
            ">=": "ge",
            "&&": "and",
            "||": "orr",
        }
        
        if op in ("==", "!=", "<", ">", "<=", ">="):
            lines = []
            lines.append(left_code)
            lines.append("    mov x1, x0")
            lines.append(f"    {right_code}")
            lines.append("    cmp x1, x0")
            lines.append(f"    cset x0, {op_map[op]}")
            return "\n    ".join(lines)
        elif op in ("&&", "||"):
            lines = []
            lines.append(left_code)
            lines.append("    mov x1, x0")
            lines.append(f"    {right_code}")
            lines.append(f"    {op_map[op]} x0, x1, x0")
            return "\n    ".join(lines)
        else:
            lines = []
            lines.append(left_code)
            lines.append("    mov x1, x0")
            lines.append(f"    {right_code}")
            lines.append(f"    {op_map[op]} x0, x1, x0")
            return "\n    ".join(lines)
    
    elif expr_type == "UNARY_OP":
        op = expr.get("operator")
        operand = expr.get("operand")
        operand_code = _generate_expr(operand, label_counter)
        if op == "-":
            return f"{operand_code}\n    neg x0, x0"
    
    elif expr_type == "CALL_EXPR":
        func_name = expr.get("name")
        args = expr.get("args", [])
        lines = []
        for i, arg in enumerate(args):
            arg_code = _generate_expr(arg, label_counter)
            lines.append(f"    {arg_code}")
            lines.append(f"    mov x{i}, x0")
        lines.append(f"    bl {func_name}")
        return "\n".join(lines)
    
    return "mov x0, 0"

# === helper functions ===
# (无，所有逻辑已委托给内部函数)

# === OOP compatibility layer ===
# 不需要，这是纯函数节点
