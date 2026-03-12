# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this module

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
def _handle_function_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 function_decl 类型节点（函数声明）。
    
    从 node 中提取函数名、返回类型、位置信息，记录到 symbol_table['functions']。
    检测重复声明并记录错误到 symbol_table['errors']。
    """
    # 提取节点信息
    func_name = node.get("value")
    return_type = node.get("data_type", "int")
    line = node.get("line", 0)
    column = node.get("column", 0)
    children = node.get("children", [])
    
    # 确保 symbol_table 的必要字段存在
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 提取参数列表（从 children 中查找 param_list 节点）
    params = _extract_params(children)
    
    # 检查函数是否已声明
    if func_name in symbol_table["functions"]:
        # 记录重复声明错误
        error = {
            "line": line,
            "column": column,
            "message": f"duplicate function declaration: {func_name}"
        }
        symbol_table["errors"].append(error)
    else:
        # 添加函数到符号表
        symbol_table["functions"][func_name] = {
            "return_type": return_type,
            "params": params,
            "line": line,
            "column": column
        }
    
    # 设置当前函数名，用于后续 return 语句检查
    symbol_table["current_function"] = func_name


# === helper functions ===
def _extract_params(children: list) -> list:
    """
    从函数声明节点的 children 中提取参数列表。
    
    遍历 children，查找 type 为 "param_list" 或 "param" 的节点，
    提取参数名和类型信息。
    """
    params = []
    
    for child in children:
        child_type = child.get("type", "")
        
        # 处理 param_list 节点
        if child_type == "param_list":
            param_children = child.get("children", [])
            for param_node in param_children:
                if param_node.get("type") == "param":
                    param_name = param_node.get("value")
                    param_type = param_node.get("data_type", "int")
                    if param_name:
                        params.append({
                            "name": param_name,
                            "type": param_type
                        })
        
        # 直接处理 param 节点（如果没有 param_list 包装）
        elif child_type == "param":
            param_name = child.get("value")
            param_type = child.get("data_type", "int")
            if param_name:
                params.append({
                    "name": param_name,
                    "type": param_type
                })
    
    return params


# === OOP compatibility layer ===
# Not needed for this helper function module