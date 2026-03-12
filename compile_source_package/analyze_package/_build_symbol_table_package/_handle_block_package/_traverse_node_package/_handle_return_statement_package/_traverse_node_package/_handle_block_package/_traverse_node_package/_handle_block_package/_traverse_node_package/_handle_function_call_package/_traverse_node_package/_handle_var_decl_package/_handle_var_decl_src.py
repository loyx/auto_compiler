# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple handler

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
    处理变量声明节点，记录变量信息到符号表。
    
    从 node 中提取变量名、数据类型、位置信息，
    并将变量信息记录到 symbol_table["variables"] 中。
    """
    # 提取变量声明信息
    var_name = node["value"]
    data_type = node["data_type"]
    line = node["line"]
    column = node["column"]
    scope_level = symbol_table["current_scope"]
    
    # 记录变量信息到符号表
    # 如果变量已存在，覆盖原有声明（允许重复声明）
    symbol_table["variables"][var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": scope_level
    }


# === helper functions ===
# No helper functions needed for this simple handler

# === OOP compatibility layer ===
# Not needed for this function node