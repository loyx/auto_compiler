# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .. import _traverse_node

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
def _handle_function_decl(node: AST, symbol_table: SymbolTable) -> None:
    """处理函数声明节点，将函数记录到符号表中。"""
    # 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []

    # 初始化 functions 字典（如果不存在）
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}

    # 提取函数信息
    func_name = node["value"]
    return_type = node["data_type"]
    line = node["line"]
    column = node["column"]

    # 保存旧的 current_function 值
    old_function = symbol_table.get("current_function", None)

    try:
        # 检查函数是否已存在
        if func_name in symbol_table["functions"]:
            # 记录重复声明错误
            symbol_table["errors"].append({
                "type": "duplicate_function",
                "message": f"Function '{func_name}' is already declared",
                "line": line,
                "column": column
            })
        else:
            # 提取参数列表（仅参数名）
            params = []
            if len(node["children"]) > 0:
                param_nodes = node["children"][0]
                if isinstance(param_nodes, list):
                    params = [p["name"] for p in param_nodes if isinstance(p, dict) and "name" in p]

            # 记录函数到符号表
            symbol_table["functions"][func_name] = {
                "return_type": return_type,
                "params": params,
                "line": line,
                "column": column
            }

        # 设置当前函数名
        symbol_table["current_function"] = func_name

        # 遍历函数体（如果存在）
        if len(node["children"]) > 1:
            body = node["children"][1]
            if isinstance(body, dict) and body.get("type") == "block":
                _traverse_node(body, symbol_table)

    finally:
        # 恢复 current_function 为旧值
        symbol_table["current_function"] = old_function


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
