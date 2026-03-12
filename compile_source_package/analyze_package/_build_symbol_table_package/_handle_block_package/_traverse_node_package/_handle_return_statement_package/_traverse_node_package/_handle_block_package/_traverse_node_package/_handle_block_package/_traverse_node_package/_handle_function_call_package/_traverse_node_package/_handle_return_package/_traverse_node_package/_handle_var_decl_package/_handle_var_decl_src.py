# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions for this module

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
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量声明节点，将变量注册到符号表中。
    
    如果变量在同一作用域内已存在，则记录重复声明错误。
    """
    # 提取变量信息
    var_name = node.get("value")
    data_type = node.get("data_type")
    line = node.get("line")
    column = node.get("column")
    
    # 确保 variables 字典存在
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 获取当前作用域层级
    current_scope = symbol_table.get("current_scope", 0)
    
    # 检查是否重复声明（同一作用域内）
    if var_name in symbol_table["variables"]:
        existing_var = symbol_table["variables"][var_name]
        if existing_var.get("scope_level") == current_scope:
            # 同一作用域内重复声明，记录错误
            error_msg = f"Duplicate declaration of variable '{var_name}' at line {line}, column {column}"
            symbol_table["errors"].append({
                "type": "duplicate_declaration",
                "message": error_msg,
                "line": line,
                "column": column,
                "variable": var_name
            })
            return
    
    # 注册变量信息到符号表
    symbol_table["variables"][var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": current_scope
    }


# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a utility function node
