# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
from ._build_symbol_table_package._build_symbol_table_src import _build_symbol_table
from ._verify_ast_package._verify_ast_src import _verify_ast

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list            # 作用域栈
# }

# === main function ===
def analyze(ast: dict, filename: str) -> dict:
    """
    语义分析：对 AST 进行类型检查和作用域验证。
    
    参数：
        ast: 语法分析产生的 AST 字典
        filename: 源文件名（用于错误报告）
    
    返回：
        验证后的 AST（与原 AST 结构相同，但节点已添加 data_type 等类型信息）
    
    异常：
        ValueError: 语义错误，消息格式为 "filename:line:column: error: message"
    """
    # 初始化符号表
    symbol_table: SymbolTable = {
        "variables": {},
        "functions": {},
        "current_scope": 0,
        "scope_stack": []
    }
    
    # 第一遍：收集所有声明
    _build_symbol_table(ast, symbol_table)
    
    # 第二遍：验证所有使用
    context_stack: List[Dict[str, Any]] = []
    _verify_ast(ast, symbol_table, context_stack, filename)
    
    return ast

# === helper functions ===
# 无，所有逻辑已委托给子函数

# === OOP compatibility layer ===
# 不需要 OOP wrapper，这是普通函数节点
