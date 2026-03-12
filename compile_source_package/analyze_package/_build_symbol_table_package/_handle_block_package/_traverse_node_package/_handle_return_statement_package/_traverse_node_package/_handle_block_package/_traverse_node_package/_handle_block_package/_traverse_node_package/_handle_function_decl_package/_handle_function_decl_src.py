# === std / third-party imports ===
from typing import Any, Dict

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
def _handle_function_decl(node: AST, symbol_table: SymbolTable) -> None:
    """处理 function_decl 类型节点，注册函数信息到符号表。"""
    # 延迟导入 _traverse_node，避免模块级别导入导致的循环依赖和缺失模块问题
    from ._traverse_node_package._traverse_node_src import _traverse_node
    
    # 初始化符号表字段（若不存在）
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 提取函数信息
    func_name = node.get("value", "")
    return_type = node.get("data_type", "int")
    line = node.get("line", -1)
    column = node.get("column", -1)
    
    # 检查是否重复声明
    if func_name in symbol_table["functions"]:
        symbol_table["errors"].append({
            "type": "error",
            "message": f"Function '{func_name}' already declared",
            "line": line,
            "column": column
        })
        return
    
    # 提取参数列表（从 children 中查找 param_list 节点）
    params = []
    children = node.get("children", [])
    for child in children:
        if child.get("type") == "param_list":
            params = child.get("children", [])
            break
    
    # 注册函数到符号表
    symbol_table["functions"][func_name] = {
        "return_type": return_type,
        "params": params,
        "line": line,
        "column": column
    }
    
    # 保存当前函数名并设置新值
    prev_function = symbol_table.get("current_function", None)
    symbol_table["current_function"] = func_name
    
    # 遍历子节点（参数声明、函数体）
    for child in children:
        _traverse_node(child, symbol_table)
    
    # 恢复之前的函数名
    symbol_table["current_function"] = prev_function


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node