# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this module

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
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量声明节点。提取变量名、类型、位置信息并注册到 symbol_table["variables"]。
    
    处理逻辑：
    1. 从 node 中提取变量信息
    2. 检查是否已声明
    3. 重复声明时记录错误，否则注册变量
    
    副作用：修改 symbol_table["variables"] 和 symbol_table["errors"]
    """
    # 提取节点信息
    var_name = node["value"]
    data_type = node["data_type"]
    line = node["line"]
    column = node["column"]
    
    # 初始化 symbol_table 字段（如果不存在）
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 获取当前作用域层级
    current_scope = symbol_table.get("current_scope", 0)
    
    # 检查变量是否已存在
    if var_name in symbol_table["variables"]:
        existing_var = symbol_table["variables"][var_name]
        # 如果已声明，记录重复声明错误
        if existing_var.get("is_declared", False):
            error = {
                "type": "duplicate_declaration",
                "message": f"Variable '{var_name}' already declared",
                "line": line,
                "column": column
            }
            symbol_table["errors"].append(error)
            return
    
    # 注册变量
    symbol_table["variables"][var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": current_scope
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
