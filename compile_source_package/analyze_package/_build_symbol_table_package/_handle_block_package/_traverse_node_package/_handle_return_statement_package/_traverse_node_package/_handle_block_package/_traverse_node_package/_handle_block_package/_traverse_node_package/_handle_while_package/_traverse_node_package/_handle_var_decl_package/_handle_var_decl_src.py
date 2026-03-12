# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple handler

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
    处理变量声明节点，将变量记录到符号表，检查重复声明。
    
    副作用：修改 symbol_table['variables']，可能记录错误到 symbol_table['errors']
    """
    # 从 node 中提取变量信息
    var_name = node.get("value")
    data_type = node.get("data_type")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 获取当前作用域层级
    current_scope = symbol_table.get("current_scope", 0)
    
    # 确保 variables 和 errors 字典存在
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 检查变量是否已声明
    if var_name in symbol_table["variables"]:
        # 记录重复声明错误
        error = {
            "type": "duplicate_declaration",
            "message": f"Variable '{var_name}' is already declared",
            "line": line,
            "column": column
        }
        symbol_table["errors"].append(error)
    else:
        # 将变量信息添加到符号表
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
