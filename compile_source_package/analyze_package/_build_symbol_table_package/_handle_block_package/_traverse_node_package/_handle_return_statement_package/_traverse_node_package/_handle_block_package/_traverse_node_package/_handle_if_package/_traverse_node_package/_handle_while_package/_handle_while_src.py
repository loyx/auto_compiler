# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", etc.)
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
    """处理 while 循环节点。"""
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 确保作用域管理字段存在
    if "scope_stack" not in symbol_table:
        symbol_table["scope_stack"] = []
    if "current_scope" not in symbol_table:
        symbol_table["current_scope"] = 0
    
    # 获取子节点
    children = node.get("children", [])
    
    # 检查子节点数量 (期望：[condition, body])
    if len(children) < 2:
        symbol_table["errors"].append({
            "line": node.get("line", 0),
            "column": node.get("column", 0),
            "message": "while node must have condition and body children"
        })
        return
    
    # 检查条件表达式类型
    condition = children[0]
    data_type = condition.get("data_type")
    if data_type != "int":
        symbol_table["errors"].append({
            "line": condition.get("line", node.get("line", 0)),
            "column": condition.get("column", node.get("column", 0)),
            "message": f"while condition must be int type, got {data_type}"
        })
        return
    
    # 进入新作用域
    symbol_table["scope_stack"].append(symbol_table["current_scope"])
    symbol_table["current_scope"] += 1
    
    # 处理循环体
    _traverse_node(children[1], symbol_table)
    
    # 退出作用域
    symbol_table["current_scope"] = symbol_table["scope_stack"].pop()

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this handler function