# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
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
#   "scope_stack": list,           # 作用域栈 (存储旧 scope 值)
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }


# === main function ===
def _handle_if(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 if 语句节点：遍历条件表达式和 then 分支（以及可选的 else 分支）。
    
    副作用：递归调用 _traverse_node 处理子节点，可能在 symbol_table["errors"] 中记录错误。
    """
    children = node.get("children", [])
    
    # 边界检查：children 为空或 None
    if not children:
        symbol_table.setdefault("errors", []).append(
            f"if statement at line {node.get('line', 'unknown')}, column {node.get('column', 'unknown')}: missing children"
        )
        return
    
    # 边界检查：至少需要条件表达式和 then 分支
    if len(children) < 2:
        symbol_table.setdefault("errors", []).append(
            f"if statement at line {node.get('line', 'unknown')}, column {node.get('column', 'unknown')}: expected at least 2 children (condition and then-branch), got {len(children)}"
        )
        return
    
    # 处理条件表达式 (children[0])
    _traverse_node(children[0], symbol_table)
    
    # 处理 then 分支 (children[1])
    _traverse_node(children[1], symbol_table)
    
    # 处理 else 分支 (children[2], 可选)
    if len(children) >= 3:
        _traverse_node(children[2], symbol_table)


# === helper functions ===
# No helper functions needed for this simple orchestration logic

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node