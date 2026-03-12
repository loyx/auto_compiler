# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "identifier")
#   "children": list,        # 子节点列表
#   "value": str,            # 标识符名称
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "name": str              # 变量名 (本函数不使用)
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
    处理 identifier 类型节点（变量引用/标识符）。
    
    验证变量是否已声明且作用域可见。
    如果未声明或作用域不可见，记录错误到 symbol_table["errors"]。
    不修改符号表结构，仅读取和可能记录错误。
    """
    # 1. 提取变量名（优先使用 "value" 字段）
    var_name = node.get("value")
    if var_name is None:
        # 节点格式错误，无法提取变量名
        symbol_table.setdefault("errors", []).append(
            f"Error: Identifier node missing 'value' field at line {node.get('line', '?')}, column {node.get('column', '?')}"
        )
        return
    
    # 2. 提取行号和列号
    line = node.get("line")
    column = node.get("column")
    
    # 如果行号/列号不存在，尝试从第一个子节点获取
    if line is None or column is None:
        children = node.get("children", [])
        if children and isinstance(children, list) and len(children) > 0:
            first_child = children[0]
            if isinstance(first_child, dict):
                if line is None:
                    line = first_child.get("line")
                if column is None:
                    column = first_child.get("column")
    
    # 如果仍无法获取，使用 "?" 占位
    line_str = str(line) if line is not None else "?"
    column_str = str(column) if column is not None else "?"
    
    # 3. 检查 symbol_table["variables"] 是否存在
    variables = symbol_table.get("variables")
    if not variables:
        # 变量表不存在，视为所有变量未声明
        symbol_table.setdefault("errors", []).append(
            f"Error: Variable '{var_name}' is not declared (no variable table) at line {line_str}, column {column_str}"
        )
        return
    
    # 4. 检查变量是否已声明
    if var_name not in variables:
        symbol_table.setdefault("errors", []).append(
            f"Error: Variable '{var_name}' is not declared at line {line_str}, column {column_str}"
        )
        return
    
    # 5. 变量已声明，检查作用域可见性
    var_info = variables[var_name]
    var_scope_level = var_info.get("scope_level", 0)
    current_scope = symbol_table.get("current_scope", 0)
    
    # 如果变量的 scope_level > current_scope，则变量在当前作用域不可见
    if var_scope_level > current_scope:
        symbol_table.setdefault("errors", []).append(
            f"Error: Variable '{var_name}' is out of scope at line {line_str}, column {column_str}"
        )
        return
    
    # 6. 变量已声明且作用域可见，验证通过，无需操作


# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# Not needed for this function node (no framework requires class wrapper)
