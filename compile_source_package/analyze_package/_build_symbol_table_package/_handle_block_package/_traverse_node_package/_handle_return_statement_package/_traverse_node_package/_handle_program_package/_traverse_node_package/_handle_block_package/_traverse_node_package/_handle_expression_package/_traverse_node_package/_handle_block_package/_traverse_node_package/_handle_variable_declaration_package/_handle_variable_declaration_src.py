# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

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
    """处理变量声明节点，注册变量到符号表并检查重复声明。"""
    # 1. 提取变量名：从 children 中查找 identifier 子节点
    var_name = None
    for child in node.get("children", []):
        if child.get("type") == "identifier":
            var_name = child.get("value")
            break

    if var_name is None:
        return  # 无有效变量名，跳过

    # 2. 检查重复声明（静默处理）
    if var_name in symbol_table.get("variables", {}):
        return  # 静默跳过重复声明

    # 3. 获取数据类型和位置信息
    data_type = node.get("data_type", "int")
    line = node.get("line", 0)
    column = node.get("column", 0)
    scope_level = symbol_table.get("current_scope", 0)

    # 4. 注册变量到符号表
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}

    symbol_table["variables"][var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": scope_level
    }

    # 5. 递归处理子节点（如初始值表达式）
    for child in node.get("children", []):
        _traverse_node(child, symbol_table)


# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# No OOP wrapper needed for this internal handler function
