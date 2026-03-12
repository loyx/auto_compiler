# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this module

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "name": str,             # 函数名 (function_call 节点使用)
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息
#   "line": int,             # 行号
#   "column": int            # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_function_call(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 function_call 类型节点。
    验证函数是否已声明，以及参数数量是否匹配。
    副作用：可能向 symbol_table['errors'] 追加错误信息。
    """
    func_name = node.get("name", "")
    children = node.get("children", [])
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 检查函数是否已声明
    functions = symbol_table.get("functions", {})
    if func_name not in functions:
        error_msg = f"Undefined function: {func_name}"
        _add_error(symbol_table, error_msg, line, column)
        return
    
    # 获取函数定义信息
    func_def = functions[func_name]
    params = func_def.get("params", [])
    
    # 检查参数数量是否匹配
    actual_arg_count = len(children)
    expected_arg_count = len(params) if params is not None else None
    
    if expected_arg_count is not None and actual_arg_count != expected_arg_count:
        error_msg = f"Function '{func_name}' expects {expected_arg_count} arguments but got {actual_arg_count}"
        _add_error(symbol_table, error_msg, line, column)

# === helper functions ===
def _add_error(symbol_table: SymbolTable, message: str, line: int, column: int) -> None:
    """
    向符号表的 errors 列表追加错误信息。
    """
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    error_entry = {
        "message": message,
        "line": line,
        "column": column
    }
    symbol_table["errors"].append(error_entry)

# === OOP compatibility layer ===
# Not needed for this function node (internal helper in AST processing pipeline)
