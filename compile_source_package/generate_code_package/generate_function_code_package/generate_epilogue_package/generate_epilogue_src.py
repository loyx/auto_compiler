# === std / third-party imports ===

# === sub function imports ===

# === ADT defines ===
# No complex ADT needed; using basic types only

# === main function ===
def generate_epilogue(stack_size: int) -> str:
    """
    生成函数出口代码（epilogue）。
    
    生成 ARM64 汇编代码用于函数退出时恢复栈帧：
    1. 恢复栈指针：mov sp, fp
    2. 恢复帧指针和返回地址：ldp fp, lr, [sp], #16
    3. 返回：ret
    
    Args:
        stack_size: 栈帧大小（已 16 字节对齐），在 epilogue 中不直接使用
    
    Returns:
        汇编代码字符串，每条指令前缀 4 个空格，每条指令独占一行
    """
    lines = [
        "    mov sp, fp",
        "    ldp fp, lr, [sp], #16",
        "    ret",
    ]
    return "\n".join(lines)

# === helper functions ===

# === OOP compatibility layer ===
