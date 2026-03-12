# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "binary_op", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (如操作符、变量名、字面量值等)
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
    处理函数声明节点。记录函数到符号表，检查重复声明。
    """
    # 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 初始化 functions 字典（如果不存在）
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    
    # 获取函数名
    func_name = node.get("value")
    if func_name is None:
        symbol_table["errors"].append({
            "type": "error",
            "message": "Function declaration missing 'value' field (function name)",
            "line": node.get("line", -1),
            "column": node.get("column", -1)
        })
        return
    
    # 获取返回类型
    return_type = node.get("data_type")
    if return_type is None:
        symbol_table["errors"].append({
            "type": "error",
            "message": f"Function declaration '{func_name}' missing 'data_type' field",
            "line": node.get("line", -1),
            "column": node.get("column", -1)
        })
        return
    
    # 检查重复声明
    if func_name in symbol_table["functions"]:
        symbol_table["errors"].append({
            "type": "error",
            "message": f"Duplicate function declaration: {func_name}",
            "line": node.get("line", -1),
            "column": node.get("column", -1)
        })
        return
    
    # 提取参数列表（从 children 中的参数声明节点）
    params = []
    children = node.get("children", [])
    for child in children:
        if child.get("type") == "param_decl":
            param_info = {
                "name": child.get("value"),
                "data_type": child.get("data_type"),
                "line": child.get("line", -1),
                "column": child.get("column", -1)
            }
            params.append(param_info)
    
    # 记录函数到符号表
    symbol_table["functions"][func_name] = {
        "return_type": return_type,
        "params": params,
        "line": node.get("line", -1),
        "column": node.get("column", -1)
    }
    
    # 设置当前函数名
    symbol_table["current_function"] = func_name

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node