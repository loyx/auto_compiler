# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", etc.)
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
def _handle_function_decl(node: AST, symbol_table: SymbolTable) -> None:
    """处理函数声明节点。"""
    func_name = node["value"]
    return_type = node["data_type"]
    line = node["line"]
    column = node["column"]

    # 检查函数是否已声明
    if func_name in symbol_table["functions"]:
        symbol_table["errors"].append({
            "type": "error",
            "line": line,
            "column": column,
            "message": f"Function '{func_name}' already declared"
        })
        return

    # 获取参数列表和函数体
    param_list_node = node["children"][0]
    body_node = node["children"][1]

    # 构建参数信息
    params = []
    for param_node in param_list_node["children"]:
        param_info = {
            "name": param_node["name"],
            "data_type": param_node["data_type"]
        }
        params.append(param_info)

    # 记录函数信息到符号表
    symbol_table["functions"][func_name] = {
        "return_type": return_type,
        "params": params,
        "line": line,
        "column": column
    }

    # 进入新作用域
    symbol_table["scope_stack"].append(symbol_table["current_scope"])
    symbol_table["current_scope"] += 1

    # 设置当前函数名
    symbol_table["current_function"] = func_name

    # 将参数作为局部变量添加到符号表
    for param_node in param_list_node["children"]:
        param_name = param_node["name"]
        symbol_table["variables"][param_name] = {
            "data_type": param_node["data_type"],
            "is_declared": True,
            "line": param_node["line"],
            "column": param_node["column"],
            "scope_level": symbol_table["current_scope"]
        }

    # 递归处理函数体
    _traverse_node(body_node, symbol_table)

    # 退出作用域
    symbol_table["current_scope"] = symbol_table["scope_stack"].pop()

    # 恢复当前函数名
    symbol_table["current_function"] = None


# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
