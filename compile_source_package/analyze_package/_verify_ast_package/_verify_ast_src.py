# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# 使用 try-except 处理导入失败，允许测试时 patch
try:
    from ._verify_node_package._verify_node_src import _verify_node
except ImportError:
    # 在测试环境中，_verify_node 将被 mock 替换
    _verify_node = None  # type: ignore

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
def _verify_ast(ast: dict, symbol_table: dict, context_stack: list, filename: str) -> None:
    """第二遍遍历：验证所有变量引用、函数调用、类型匹配。"""
    _verify_node(ast, symbol_table, context_stack, filename)

# === helper functions ===
# (所有具体逻辑已委托给 _verify_node 子函数)

# === OOP compatibility layer ===
# 不需要 OOP wrapper（这是内部工具函数）
