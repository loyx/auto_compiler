# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple parsing logic

# === ADT defines ===
CompilerConfig = Dict[str, Any]
# CompilerConfig possible fields:
# {
#   "source_file": str,      # 源文件路径
#   "output_file": str | None,  # 输出文件路径，None 表示 stdout
#   "verbose": bool          # 是否详细输出
# }

# === main function ===
def parse_arguments(args: list) -> CompilerConfig:
    """
    解析命令行参数（gcc 风格），返回配置对象。
    
    支持的参数：
    - 位置参数：源文件路径（必需）
    - -o <file>: 指定输出文件（可选）
    - -v: 详细输出模式（可选）
    
    参数错误时抛出 ValueError。
    """
    config: CompilerConfig = {
        "source_file": None,
        "output_file": None,
        "verbose": False
    }
    
    i = 0
    positional_count = 0
    
    while i < len(args):
        arg = args[i]
        
        if arg == "-o":
            if i + 1 >= len(args):
                raise ValueError("选项 -o 后必须指定输出文件路径")
            config["output_file"] = args[i + 1]
            i += 2
        elif arg == "-v":
            config["verbose"] = True
            i += 1
        elif arg.startswith("-"):
            raise ValueError(f"未知选项：{arg}")
        else:
            # 位置参数（源文件）
            config["source_file"] = arg
            positional_count += 1
            i += 1
    
    if config["source_file"] is None:
        raise ValueError("必须指定源文件路径")
    
    if positional_count > 1:
        raise ValueError("只能指定一个源文件")
    
    return config

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node