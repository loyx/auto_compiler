# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .generate_statement_code_package.generate_statement_code_src import generate_statement_code
from .calculate_stack_size_package.calculate_stack_size_src import calculate_stack_size
from .generate_prologue_package.generate_prologue_src import generate_prologue
from .generate_epilogue_package.generate_epilogue_src import generate_epilogue
from .build_var_offsets_package.build_var_offsets_src import build_var_offsets

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "name": str,
#   "params": list,
#   "return_type": str,
#   "body": list,
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

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

# === main function ===
def generate_function_code(func_def: dict, label_counter: dict) -> str:
    """生成单个函数的 ARM64 汇编代码。"""
    func_name = func_def["name"]
    params = func_def.get("params", [])
    body = func_def.get("body", [])
    return_type = func_def.get("return_type", "void")
    
    # 计算局部变量数量（遍历 body 统计 VAR_DECL）
    local_var_count = _count_local_vars(body)
    
    # 计算栈帧大小（16 字节对齐）
    stack_size = calculate_stack_size(len(params), local_var_count)
    
    # 生成函数入口
    code_lines = [f"{func_name}:"]
    prologue = generate_prologue(func_name, stack_size)
    code_lines.append(prologue)
    
    # 构建变量偏移字典（参数从 sp+16 开始）
    param_start_offset = 16
    var_offsets, _ = build_var_offsets(params, param_start_offset)
    
    # 生成函数体代码
    for stmt in body:
        stmt_code = generate_statement_code(stmt, func_name, label_counter, var_offsets)
        code_lines.append(stmt_code)
    
    # 检查是否需要默认返回（非 void 且无显式 return）
    has_return = _has_explicit_return(body)
    if return_type != "void" and not has_return:
        code_lines.append(f"    mov x0, #0")
    
    # 添加出口标签和 epilogue
    code_lines.append(f"{func_name}_exit:")
    epilogue = generate_epilogue(stack_size)
    code_lines.append(epilogue)
    
    return "\n".join(code_lines)

# === helper functions ===
def _count_local_vars(body: list) -> int:
    """统计函数体中 VAR_DECL 语句的数量。"""
    count = 0
    for stmt in body:
        if stmt.get("type") == "VAR_DECL":
            count += 1
    return count

def _has_explicit_return(body: list) -> bool:
    """检查函数体是否包含显式 RETURN 语句。"""
    for stmt in body:
        if stmt.get("type") == "RETURN":
            return True
    return False

# === OOP compatibility layer ===
