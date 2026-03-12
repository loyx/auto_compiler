# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple semantic analysis

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
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 var_decl 类型节点的语义分析（变量声明）。
    
    从 AST 节点提取变量信息，检查重复声明，注册变量到符号表。
    """
    # 提取节点信息
    name = node.get("name", "")
    data_type = node.get("data_type", "int")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 获取当前作用域层级（默认 0）
    current_scope = symbol_table.get("current_scope", 0)
    
    # 确保 variables 和 errors 已初始化
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 检查变量是否已在同一作用域声明
    if name in symbol_table["variables"]:
        existing_var = symbol_table["variables"][name]
        if existing_var.get("scope_level") == current_scope:
            # 同一作用域重复声明，记录错误
            error = {
                "type": "error",
                "message": f"Variable '{name}' already declared",
                "line": line,
                "column": column
            }
            symbol_table["errors"].append(error)
            return
    
    # 注册变量到符号表
    symbol_table["variables"][name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": current_scope
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node (semantic analysis utility)
