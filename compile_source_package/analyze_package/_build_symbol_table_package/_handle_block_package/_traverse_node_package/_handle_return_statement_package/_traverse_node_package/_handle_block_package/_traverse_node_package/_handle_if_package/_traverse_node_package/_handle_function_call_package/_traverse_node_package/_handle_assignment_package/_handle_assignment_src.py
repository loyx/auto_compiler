# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", "literal", "identifier", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "name": str,             # 名称 (function_call / identifier 节点使用)
#   "value": Any,            # 节点值 (literal 节点使用)
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
#   "errors": list                 # 错误列表 (保证已初始化为 [])
# }

# === main function ===
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """处理 assignment 类型节点的语义分析（赋值语句）。"""
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 获取赋值目标 target（通常是 identifier 节点）
    target = node.get("target")
    if not target:
        symbol_table["errors"].append({
            "type": "error",
            "message": "Assignment target missing",
            "line": line,
            "column": column
        })
        return
    
    # 从 target 中提取变量名
    var_name = target.get("name")
    if not var_name:
        symbol_table["errors"].append({
            "type": "error",
            "message": "Assignment target has no name",
            "line": line,
            "column": column
        })
        return
    
    # 检查变量是否已声明
    variables = symbol_table.get("variables", {})
    if var_name not in variables:
        symbol_table["errors"].append({
            "type": "error",
            "message": f"Assignment to undeclared variable: {var_name}",
            "line": line,
            "column": column
        })
        return
    
    # 变量已声明，可选检查类型匹配
    var_info = variables[var_name]
    declared_type = var_info.get("data_type")
    
    # 获取赋值表达式的值节点
    value_node = node.get("value")
    if value_node:
        # 递归遍历 value 子节点进行语义分析
        _traverse_node(value_node, symbol_table)
        
        # 可选：检查类型匹配（如果 value 节点有 data_type 信息）
        if declared_type and value_node.get("data_type"):
            value_type = value_node.get("data_type")
            if declared_type != value_type:
                symbol_table["errors"].append({
                    "type": "error",
                    "message": f"Type mismatch: assigning {value_type} to {declared_type} variable '{var_name}'",
                    "line": line,
                    "column": column
                })

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node