# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("var_decl")
#   "children": list,        # 子节点列表 (可选)
#   "value": Any,            # 节点值 (可能包含变量名)
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int,           # 列号
#   "name": str,             # 变量名 (可选)
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
    
    从 AST 节点中提取变量名、类型信息，检查是否重复声明，
    记录到 symbol_table['variables']。
    
    副作用：修改 symbol_table['variables']，可能添加错误到 symbol_table['errors']
    """
    # 1. 提取变量名（优先从 "name" 字段，其次 "value" 字段）
    var_name = node.get("name")
    if var_name is None:
        var_name = node.get("value")
    
    if var_name is None:
        # 无法提取变量名，记录错误
        error_msg = f"Cannot extract variable name at line {node.get('line', 'unknown')}, column {node.get('column', 'unknown')}"
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append(error_msg)
        return
    
    # 2. 提取数据类型（默认为 "int"）
    data_type = node.get("data_type", "int")
    
    # 3. 提取行号和列号
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 4. 获取当前作用域层级
    current_scope = symbol_table.get("current_scope", 0)
    
    # 5. 检查变量是否已声明
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    if var_name in symbol_table["variables"]:
        # 6. 已声明，记录重复声明错误
        existing_info = symbol_table["variables"][var_name]
        error_msg = f"Variable '{var_name}' already declared at line {existing_info.get('line', 'unknown')}, column {existing_info.get('column', 'unknown')}"
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append(error_msg)
    else:
        # 7. 未声明，添加到符号表
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
# Not needed for this internal function