# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# 延迟导入 _verify_node 从父级模块（在函数内部导入以避免循环依赖）

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("while_stmt" 或 "for_stmt")
#   "condition": dict,       # 条件表达式
#   "body": dict,            # 循环体
#   "init": dict,            # for_stmt 专用：初始化表达式
#   "update": dict,          # for_stmt 专用：更新表达式
#   "line": int,             # 行号
#   "column": int            # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
# }

ContextStack = list
# ContextStack possible fields:
# [
#   {"type": "function", "name": str, "return_type": str},
#   {"type": "loop", "stmt_type": "while"|"for"}
# ]


# === main function ===
def _verify_loop_stmt(node: dict, symbol_table: dict, context_stack: list, filename: str) -> None:
    """
    验证 while_stmt 和 for_stmt 节点。
    
    处理流程：
    1. while_stmt: 验证 condition → push loop 帧 → 验证 body → pop 帧
    2. for_stmt: 验证 init → 验证 condition → push loop 帧 → 验证 body → pop 帧 → 验证 update
    """
    # 延迟导入以避免循环依赖
    from ..._verify_node_package._verify_node_src import _verify_node
    
    node_type = node["type"]
    line = node.get("line", "?")
    column = node.get("column", "?")
    
    # 延迟导入以避免循环依赖
    from .._verify_node_src import _verify_node
    
    if node_type == "while_stmt":
        # 验证条件表达式
        _verify_node(node["condition"], symbol_table, context_stack, filename)
        
        # 压入 loop 帧
        context_stack.append({"type": "loop", "stmt_type": "while"})
        
        try:
            # 验证循环体
            _verify_node(node["body"], symbol_table, context_stack, filename)
        finally:
            # 弹出栈帧，确保平衡
            context_stack.pop()
    
    elif node_type == "for_stmt":
        # 验证初始化表达式
        _verify_node(node["init"], symbol_table, context_stack, filename)
        
        # 验证条件表达式
        _verify_node(node["condition"], symbol_table, context_stack, filename)
        
        # 压入 loop 帧
        context_stack.append({"type": "loop", "stmt_type": "for"})
        
        try:
            # 验证循环体
            _verify_node(node["body"], symbol_table, context_stack, filename)
        finally:
            # 弹出栈帧，确保平衡
            context_stack.pop()
        
        # 验证更新表达式
        _verify_node(node["update"], symbol_table, context_stack, filename)
    
    else:
        # 理论上不会发生，由 _verify_node 保证分发
        raise ValueError(f"{filename}:{line}:{column}: 未知的循环语句类型 {node_type}")


# === helper functions ===
# 无 helper 函数，逻辑已在主函数中完成

# === OOP compatibility layer ===
# 本模块为普通函数节点，无需 OOP wrapper
