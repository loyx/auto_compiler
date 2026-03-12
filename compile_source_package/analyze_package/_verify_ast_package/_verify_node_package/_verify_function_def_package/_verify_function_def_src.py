# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Import main coordinator for recursive verification
# (imported inside function to avoid circular import)

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("function_def")
#   "name": str,             # 函数名
#   "params": list,          # 参数列表
#   "body": dict,            # 函数体（AST 节点）
#   "line": int,             # 行号
#   "column": int            # 列号
#   "return_type": str       # 返回类型（可选）
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
def _verify_function_def(node: dict, symbol_table: dict, context_stack: list, filename: str) -> None:
    """
    处理函数定义节点。
    将 function 帧压入 context_stack，递归验证 body，然后弹出栈帧。
    """
    # 1. 验证必要字段
    if "name" not in node:
        line = node.get("line", 0)
        column = node.get("column", 0)
        raise ValueError(f"{filename}:{line}:{column}: error: function definition missing name")

    # 2. 压入 function context 帧
    context_stack.append({
        "type": "function",
        "name": node["name"],
        "return_type": node.get("return_type", "void")
    })

    try:
        # 3. 递归验证函数体（如果存在）
        if node.get("body"):
            from .._verify_node_src import _verify_node
            _verify_node(node["body"], symbol_table, context_stack, filename)
    finally:
        # 4. 弹出 context 帧（确保清理）
        context_stack.pop()


# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed - this is a verification function, not a framework entry point
