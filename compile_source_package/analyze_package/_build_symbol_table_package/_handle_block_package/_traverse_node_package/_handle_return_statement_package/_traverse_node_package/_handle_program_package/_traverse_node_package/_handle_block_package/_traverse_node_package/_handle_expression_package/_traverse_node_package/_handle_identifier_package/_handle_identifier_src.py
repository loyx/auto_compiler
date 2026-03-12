# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub-functions needed

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block" 等)
#   "children": list,        # 子节点列表
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
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }


# === main function ===
def _handle_identifier(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 identifier 节点：检查变量是否已声明。
    
    如果变量未声明，记录未定义变量错误到 symbol_table["errors"]。
    副作用：可能修改 symbol_table (添加错误记录)。
    """
    # 1. 获取标识符名称
    var_name = node.get("value")
    if not var_name:
        return
    
    # 2. 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 3. 确保 variables 字典存在
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # 4. 检查变量是否已声明
    if var_name not in symbol_table["variables"]:
        # 5. 记录未定义变量错误
        symbol_table["errors"].append({
            "type": "undefined_variable",
            "message": f"Variable '{var_name}' is not declared",
            "line": node.get("line", 0),
            "column": node.get("column", 0),
            "node_type": "identifier"
        })


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
