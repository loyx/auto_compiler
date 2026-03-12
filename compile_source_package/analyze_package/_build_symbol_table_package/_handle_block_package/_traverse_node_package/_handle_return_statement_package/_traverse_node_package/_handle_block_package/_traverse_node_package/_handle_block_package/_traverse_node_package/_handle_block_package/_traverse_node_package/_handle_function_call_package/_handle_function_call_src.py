# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# _traverse_node is a sibling function in the same module, no import needed

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (函数名、变量名、字面量等)
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
def _handle_function_call(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理函数调用节点：验证函数存在并处理参数。
    """
    # 初始化错误列表
    if "errors" not in symbol_table:
        symbol_table["errors"] = []

    # 提取函数名和位置信息
    func_name = node.get("value", "")
    line = node.get("line", -1)
    column = node.get("column", -1)

    # 检查函数是否已声明
    if "functions" not in symbol_table or func_name not in symbol_table["functions"]:
        error_entry = {
            "type": "error",
            "message": f"Undefined function: {func_name}",
            "line": line,
            "column": column
        }
        symbol_table["errors"].append(error_entry)
        # 即使函数未定义，仍需遍历参数以发现更多错误
    else:
        # 验证参数数量
        func_decl = symbol_table["functions"][func_name]
        expected_count = len(func_decl.get("params", []))
        actual_count = len(node.get("children", []))

        if expected_count != actual_count:
            error_entry = {
                "type": "error",
                "message": f"Function '{func_name}' expects {expected_count} arguments, got {actual_count}",
                "line": line,
                "column": column
            }
            symbol_table["errors"].append(error_entry)

    # 遍历所有参数表达式
    for arg in node.get("children", []):
        _traverse_node(arg, symbol_table)


# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
