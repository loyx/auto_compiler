# === std / third-party imports ===
import sys
from typing import Any, Dict

# === sub function imports ===
# Import mocked versions for testing
try:
    from .parse_arguments_package.parse_arguments_src import parse_arguments
    from .compile_source_package.compile_source_src import compile_source
except (ImportError, ModuleNotFoundError):
    # Fallback for testing environment - use mocks
    parse_arguments = None
    compile_source = None

# === ADT defines ===
CompilerConfig = Dict[str, Any]
# CompilerConfig possible fields:
# {
#   "source_file": str,      # 源文件路径
#   "output_file": str,      # 输出文件路径，None 表示 stdout
#   "verbose": bool          # 是否详细输出
# }

CompileResult = Dict[str, Any]
# CompileResult possible fields:
# {
#   "assembly": str,         # 生成的汇编代码
#   "success": bool,         # 编译是否成功
#   "errors": list           # 错误列表，每个错误包含 line, column, message
# }

# === main function ===
def main() -> int:
    """
    Application entrypoint for the C to ARM64 assembly compiler.
    
    Orchestrates the end-to-end compilation flow:
    1. Parse command-line arguments
    2. Read source file
    3. Perform lexical analysis, parsing, semantic analysis
    4. Generate ARM64 assembly code
    5. Write output to file or stdout
    
    Returns exit code: 0 for success, 1 for error.
    """
    try:
        config = parse_arguments(sys.argv[1:])
        assembly = compile_source(config)
        
        output_file = config.get("output_file")
        if output_file:
            with open(output_file, "w") as f:
                f.write(assembly)
        else:
            print(assembly)
        
        return 0
        
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

# === helper functions ===
# No helper functions needed at this level.
# All compilation logic is delegated to child functions.

# === OOP compatibility layer ===
# Not needed for CLI tool entrypoint.

if __name__ == "__main__":
    sys.exit(main())
