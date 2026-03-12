# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this implementation

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
    处理变量声明节点。
    
    从节点提取变量名和类型信息，检查是否重复声明，
    并注册到符号表或记录错误。
    """
    # 确保 variables 和 errors 初始化
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 提取变量名
    var_name = node.get("value")
    if var_name is None:
        error_entry = {
            "type": "error",
            "message": "Variable declaration missing name",
            "line": node.get("line", -1),
            "column": node.get("column", -1)
        }
        symbol_table["errors"].append(error_entry)
        return
    
    # 提取数据类型（默认为 "int"）
    data_type = node.get("data_type", "int")
    
    # 获取当前作用域层级
    current_scope = symbol_table.get("current_scope", 0)
    
    # 检查变量是否已声明
    if var_name in symbol_table["variables"]:
        existing_var = symbol_table["variables"][var_name]
        # 检查是否在同一作用域
        if existing_var.get("scope_level") == current_scope:
            error_entry = {
                "type": "error",
                "message": f"Variable '{var_name}' already declared",
                "line": node.get("line", -1),
                "column": node.get("column", -1)
            }
            symbol_table["errors"].append(error_entry)
            return
    
    # 注册变量到符号表
    symbol_table["variables"][var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": node.get("line", -1),
        "column": node.get("column", -1),
        "scope_level": current_scope
    }


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function