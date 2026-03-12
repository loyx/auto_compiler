# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this module

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
def _handle_function_call(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 function_call 类型节点。
    
    验证函数是否已声明，检查参数数量是否匹配。
    副作用：可能向 symbol_table["errors"] 追加错误记录。
    """
    # 1. 从 node 中提取关键信息
    func_name = node["value"]
    line = node["line"]
    column = node["column"]
    arg_nodes = node.get("children", [])
    arg_count = len(arg_nodes)
    
    # 2. 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 3. 检查函数是否已声明
    functions = symbol_table.get("functions", {})
    
    if func_name not in functions:
        # 函数未声明，记录错误
        error = {
            "type": "undefined_function",
            "message": f"Function '{func_name}' is not defined",
            "line": line,
            "column": column
        }
        symbol_table["errors"].append(error)
        return
    
    # 4. 函数已声明，可选：检查参数数量是否匹配
    func_decl = functions[func_name]
    declared_params = func_decl.get("params", [])
    
    # 如果 params 字段存在且可确定参数数量
    if isinstance(declared_params, list):
        declared_count = len(declared_params)
        if arg_count != declared_count:
            error = {
                "type": "argument_count_mismatch",
                "message": f"Argument count mismatch for function '{func_name}'",
                "line": line,
                "column": column
            }
            symbol_table["errors"].append(error)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node