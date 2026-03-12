# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this module

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "data_type": str,
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_variable_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量声明节点，注册变量到符号表。
    
    处理逻辑：
    1. 从 node 中提取变量名和数据类型
    2. 检查变量是否已在当前作用域声明
    3. 若已声明，记录重定义错误
    4. 若未声明，注册到 symbol_table["variables"]
    """
    var_name = node["value"]
    data_type = node["data_type"]
    current_scope = symbol_table["current_scope"]
    
    # 确保 errors 列表已初始化
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 确保 variables 字典已初始化
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # 检查当前作用域是否已存在同名变量
    existing_var = symbol_table["variables"].get(var_name)
    if existing_var is not None and existing_var.get("scope_level") == current_scope:
        # 同一作用域内重复声明，记录错误
        error = {
            "type": "variable_redeclaration",
            "message": f"变量 '{var_name}' 已在当前作用域声明",
            "line": node.get("line"),
            "column": node.get("column")
        }
        symbol_table["errors"].append(error)
        return
    
    # 注册变量到符号表（允许 shadowing：父作用域变量可被覆盖）
    symbol_table["variables"][var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": node.get("line"),
        "column": node.get("column"),
        "scope_level": current_scope
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
