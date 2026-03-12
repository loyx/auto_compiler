# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "func_call", etc.)
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
def _handle_func_call(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理函数调用节点：验证函数已声明且参数数量匹配。
    
    Args:
        node: func_call 类型的 AST 节点
        symbol_table: 符号表，用于验证函数
    
    Side effects:
        可能向 symbol_table["errors"] 添加错误记录
    """
    func_name = node.get("value")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 获取实参列表
    actual_args = node.get("children", [])
    actual_arg_count = len(actual_args)
    
    # 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 查找函数声明
    functions = symbol_table.get("functions", {})
    
    if func_name not in functions:
        # 函数未声明
        error = {
            "type": "undeclared_function",
            "message": f"Function '{func_name}' is not declared",
            "line": line,
            "column": column
        }
        symbol_table["errors"].append(error)
        return
    
    # 函数已声明，检查参数数量
    func_decl = functions[func_name]
    formal_params = func_decl.get("params", [])
    expected_arg_count = len(formal_params)
    
    if actual_arg_count != expected_arg_count:
        error = {
            "type": "parameter_count_mismatch",
            "message": f"Function '{func_name}' expects {expected_arg_count} arguments, got {actual_arg_count}",
            "line": line,
            "column": column
        }
        symbol_table["errors"].append(error)


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node