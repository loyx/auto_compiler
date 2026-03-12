# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple handler

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "name": str,             # 变量名 (var_decl 节点使用)
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量声明节点。
    
    检查变量是否重复声明，注册变量到符号表。
    副作用：更新 symbol_table['variables']，可能追加错误到 symbol_table['errors']
    """
    # 1. 从 node 获取变量信息
    var_name = node.get("name")
    data_type = node.get("data_type")
    line = node.get("line")
    column = node.get("column")
    
    # 2. 检查变量是否已在 symbol_table["variables"] 中声明
    variables = symbol_table.get("variables", {})
    
    if var_name in variables:
        # 3. 如果已声明，追加错误
        error_msg = f"Variable '{var_name}' already declared at line {line}"
        symbol_table.setdefault("errors", []).append(error_msg)
    else:
        # 4. 如果未声明，将变量注册到 symbol_table["variables"]
        current_scope = symbol_table.get("current_scope", 0)
        variables[var_name] = {
            "data_type": data_type,
            "is_declared": True,
            "line": line,
            "column": column,
            "scope_level": current_scope
        }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function node
