# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple handler

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
    处理变量声明节点，将变量信息记录到符号表。
    
    如果变量在同一作用域已声明，记录错误到 symbol_table['errors']。
    如果变量未声明，将变量信息添加到 symbol_table['variables']。
    """
    # 从节点提取信息
    var_name = node["value"]
    data_type = node["data_type"]
    line = node["line"]
    column = node["column"]
    current_scope = symbol_table["current_scope"]
    
    # 检查变量是否已在当前作用域声明
    if var_name in symbol_table["variables"]:
        existing_var = symbol_table["variables"][var_name]
        if existing_var.get("scope_level") == current_scope:
            # 同一作用域重复声明，记录错误
            error_msg = f"Variable '{var_name}' already declared at line {line}, column {column}"
            symbol_table["errors"].append(error_msg)
            return
    
    # 变量未在当前作用域声明，添加到符号表
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
# No OOP wrapper needed for this function node