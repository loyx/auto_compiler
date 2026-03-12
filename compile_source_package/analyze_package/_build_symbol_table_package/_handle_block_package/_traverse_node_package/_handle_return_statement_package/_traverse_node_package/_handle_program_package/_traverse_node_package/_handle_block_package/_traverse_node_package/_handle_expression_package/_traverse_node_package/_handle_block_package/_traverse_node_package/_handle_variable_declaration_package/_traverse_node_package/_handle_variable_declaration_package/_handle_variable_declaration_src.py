# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple operation

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
def _handle_variable_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量声明节点，将变量信息注册到符号表中。
    
    处理逻辑：
    1. 从 node 中提取变量名（可能在 "name" 或 "value" 字段中）
    2. 从 node 中提取数据类型（"data_type" 字段，默认为 "int"）
    3. 从 node 中提取位置信息（"line" 和 "column" 字段）
    4. 从 symbol_table 获取当前作用域层级（"current_scope" 字段）
    5. 在 symbol_table["variables"] 中注册变量
    """
    # 确保 symbol_table["variables"] 存在
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # 提取变量名（优先从 "name" 字段，其次从 "value" 字段）
    var_name = node.get("name") or node.get("value")
    if var_name is None:
        return  # 无法提取变量名，静默跳过
    
    # 提取数据类型（默认为 "int"）
    data_type = node.get("data_type", "int")
    
    # 提取位置信息
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 获取当前作用域层级
    current_scope = symbol_table.get("current_scope", 0)
    
    # 注册变量到符号表
    symbol_table["variables"][var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": current_scope
    }


# === helper functions ===
# No helper functions needed for this simple operation

# === OOP compatibility layer ===
# Not needed for this internal helper function