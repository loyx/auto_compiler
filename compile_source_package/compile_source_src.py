# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .lex_package.lex_src import lex
from .parse_package.parse_src import parse
from .analyze_package.analyze_src import analyze
from .generate_code_package.generate_code_src import generate_code

# === ADT defines ===
CompilerConfig = Dict[str, Any]
# CompilerConfig possible fields:
# {
#   "source_file": str,      # 源文件路径（必填）
#   "output_file": str,      # 输出文件路径（可选，None 表示 stdout）
#   "verbose": bool          # 是否详细输出（可选）
# }

Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点
#   "value": Any             # 节点值
# }

# === main function ===
def compile_source(config: CompilerConfig) -> str:
    """执行完整编译流程：读取源码 → 词法分析 → 语法分析 → 语义分析 → 代码生成。"""
    source_file = config["source_file"]
    
    # 读取源码
    with open(source_file, "r", encoding="utf-8") as f:
        source = f.read()
    
    # 词法分析
    tokens = lex(source, source_file)
    
    # 语法分析
    ast = parse(tokens, source_file)
    
    # 语义分析
    validated_ast = analyze(ast, source_file)
    
    # 代码生成
    assembly = generate_code(validated_ast)
    
    return assembly

# === helper functions ===
def _create_error(filename: str, line: int, column: int, message: str) -> str:
    """生成标准格式的错误信息。"""
    return f"{filename}:{line}:{column}: error: {message}"

# === OOP compatibility layer ===
# 本模块为普通函数节点，不需要 OOP wrapper