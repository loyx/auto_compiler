# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# 导入分发器用于递归遍历子节点
from .._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "name": str,             # 函数名
#   "params": list,          # 参数列表
#   "body": AST,             # 函数体
#   "return_type": str,      # 返回类型
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,
#   "scope_stack": list
# }

# === main function ===
def _handle_for_loop(node: AST, symbol_table: SymbolTable) -> None:
    """处理 for 循环节点。
    
    从节点中提取 iterator、iterable、body 字段，
    递归遍历 iterable 表达式和循环体。
    
    Args:
        node: for_loop 类型的 AST 节点
        symbol_table: 符号表，会被递归遍历过程修改
    """
    iterator = node.get("iterator")  # str, 迭代变量名
    iterable = node.get("iterable")  # AST, 迭代对象表达式
    body = node.get("body")  # AST, 循环体
    
    # 可选：将 iterator 注册为循环作用域变量
    # 具体注册逻辑由符号表管理策略决定，此处暂不实现
    
    # 递归遍历 iterable 表达式（如果 iterable 是 AST 节点）
    if isinstance(iterable, dict):
        _traverse_node(iterable, symbol_table)
    
    # 递归遍历循环体
    if isinstance(body, dict):
        _traverse_node(body, symbol_table)

# === helper functions ===
# 无 helper 函数，逻辑已在主函数中完成

# === OOP compatibility layer ===
# 不需要 OOP wrapper，此为纯函数节点
