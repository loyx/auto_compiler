# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

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
def _handle_while(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理循环语句（while）节点。
    
    处理逻辑：
    1. 从 node 中提取 children 列表
    2. 第一个子节点是条件表达式
    3. 第二个子节点是循环体（通常是 block 类型）
    4. 调用 _traverse_node 递归处理每个子节点
    """
    children = node.get("children", [])
    
    if len(children) < 2:
        line = node.get("line", "unknown")
        column = node.get("column", "unknown")
        symbol_table.setdefault("errors", []).append(
            f"While statement at line {line}, column {column} has insufficient children"
        )
        return
    
    condition_expr = children[0]
    loop_body = children[1]
    
    # 处理条件表达式
    _traverse_node(condition_expr, symbol_table)
    
    # 处理循环体
    _traverse_node(loop_body, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
