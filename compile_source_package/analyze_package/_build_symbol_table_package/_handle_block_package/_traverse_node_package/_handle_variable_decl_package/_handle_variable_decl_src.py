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
#   "value": Any,            # 节点值（变量名可能在此）
#   "name": str,             # 变量名（也可能在此字段）
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
#   "scope_stack": list            # 作用域栈
# }

VariableRecord = Dict[str, Any]
# VariableRecord possible fields:
# {
#   "data_type": str,        # 变量数据类型
#   "is_declared": bool,     # 是否已声明
#   "line": int,             # 声明行号
#   "column": int,           # 声明列号
#   "scope_level": int       # 作用域层级
# }

# === main function ===
def _handle_variable_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 variable_decl 类型节点，将变量声明注册到符号表中。
    
    从 node 中提取变量名、数据类型、位置信息，
    并在 symbol_table["variables"] 中添加变量记录。
    """
    # 提取变量名（优先从 "value" 字段，其次从 "name" 字段）
    var_name = node.get("value")
    if var_name is None:
        var_name = node.get("name")
    if var_name is None:
        return  # 无法提取变量名，跳过处理
    
    # 提取数据类型
    data_type = node.get("data_type", "int")
    
    # 提取位置信息
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 获取当前作用域层级
    scope_level = symbol_table.get("current_scope", 0)
    
    # 构建变量记录
    var_record: VariableRecord = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": scope_level
    }
    
    # 注册到符号表（如果已存在则覆盖）
    symbol_table["variables"][var_name] = var_record

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this internal handler function
