# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", "function_decl", "param_list", "param", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值
#   "name": str,             # 变量名或函数名 (可选，用于 var_decl)
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
#   "errors": list                 # 错误列表 [{type, message, line, column}]
# }


# === main function ===
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量声明节点，将变量信息记录到符号表中。
    
    检测同一作用域内的重复声明并记录错误。
    不同作用域的同名变量允许（变量遮蔽）。
    """
    # 确保必要字段已初始化
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    if "current_scope" not in symbol_table:
        symbol_table["current_scope"] = 0
    
    # 提取变量信息
    var_name = node.get("name") or node.get("value")
    data_type = node.get("data_type", "int")
    line = node.get("line", 0)
    column = node.get("column", 0)
    current_scope = symbol_table["current_scope"]
    
    # 检查是否已存在同名变量
    if var_name in symbol_table["variables"]:
        existing = symbol_table["variables"][var_name]
        if existing["scope_level"] == current_scope:
            # 同一作用域内的重复声明 → 错误，不更新记录
            error_record = {
                "type": "error",
                "message": f"Duplicate declaration of variable '{var_name}' at line {line}, column {column}",
                "line": line,
                "column": column
            }
            symbol_table["errors"].append(error_record)
            return
        # 不同作用域 → 允许遮蔽，继续更新记录
    
    # 添加或更新变量记录
    symbol_table["variables"][var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": current_scope
    }


# === helper functions ===

# === OOP compatibility layer ===
