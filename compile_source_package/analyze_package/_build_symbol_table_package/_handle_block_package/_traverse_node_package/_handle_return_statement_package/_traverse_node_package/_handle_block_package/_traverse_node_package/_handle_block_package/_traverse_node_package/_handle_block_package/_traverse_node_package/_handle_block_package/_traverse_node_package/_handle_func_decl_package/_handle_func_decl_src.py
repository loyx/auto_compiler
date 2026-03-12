# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this module

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
def _handle_func_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理函数声明节点。
    
    从 node 中提取函数名、返回类型、参数列表等信息，
    注册到 symbol_table["functions"] 中。
    如果函数已声明，记录重复声明错误到 symbol_table["errors"]。
    """
    # 确保 symbol_table["functions"] 存在
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    
    # 确保 symbol_table["errors"] 存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 从 node 中提取基本信息
    func_name = node.get("value")
    return_type = node.get("data_type", "int")
    line = node.get("line", 0)
    column = node.get("column", 0)
    children = node.get("children", [])
    
    # 从 children 中提取参数列表（第一个 child 通常是参数列表）
    params = []
    for child in children:
        if child.get("type") == "param_list":
            for param in child.get("children", []):
                if param.get("type") == "param":
                    params.append({
                        "name": param.get("value"),
                        "data_type": param.get("data_type", "int")
                    })
            break
    
    # 检查函数是否已声明
    if func_name in symbol_table["functions"]:
        # 记录重复声明错误
        error_msg = f"Function '{func_name}' already declared at line {line}, column {column}"
        symbol_table["errors"].append({
            "type": "duplicate_function_declaration",
            "message": error_msg,
            "line": line,
            "column": column,
            "function_name": func_name
        })
    else:
        # 注册函数信息到符号表
        symbol_table["functions"][func_name] = {
            "return_type": return_type,
            "params": params,
            "line": line,
            "column": column
        }


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node