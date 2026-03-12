# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .._traverse_node_src import _traverse_node

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
    处理 while 循环语句节点。
    
    验证 while 节点必须有 2 个子节点（条件表达式、循环体），
    然后递归遍历它们。while 不引入新作用域。
    """
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 验证 children 结构
    children = node.get("children", [])
    if not children or len(children) < 2:
        error_entry = {
            "type": "error",
            "message": "While node must have 2 children (condition, body)",
            "line": node.get("line", -1),
            "column": node.get("column", -1)
        }
        symbol_table["errors"].append(error_entry)
        return
    
    # 递归处理条件表达式和循环体（不改变作用域）
    _traverse_node(children[0], symbol_table)  # condition
    _traverse_node(children[1], symbol_table)  # body


# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a plain function node
