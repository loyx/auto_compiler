# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "binary_op", "function_call", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (如操作符、变量名、字面量值、函数名等)
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
    处理函数调用节点。检查函数是否已声明，验证参数数量和类型。
    
    副作用：可能记录错误到 symbol_table['errors']，并递归遍历参数节点。
    异常：不抛出异常。
    """
    # 检查 value 字段是否存在
    if "value" not in node:
        error = {
            "type": "error",
            "message": "Function call node missing 'value' field",
            "line": node.get("line", -1),
            "column": node.get("column", -1)
        }
        symbol_table.setdefault("errors", []).append(error)
        return
    
    func_name = node["value"]
    line = node.get("line", -1)
    column = node.get("column", -1)
    
    # 检查函数是否已声明
    functions = symbol_table.get("functions", {})
    if func_name not in functions:
        error = {
            "type": "error",
            "message": f"Call to undeclared function: {func_name}",
            "line": line,
            "column": column
        }
        symbol_table.setdefault("errors", []).append(error)
        return
    
    # 获取函数声明信息
    func_decl = functions[func_name]
    declared_params = func_decl.get("params", [])
    
    # 获取实际参数列表
    actual_args = node.get("children", [])
    
    # 验证参数数量
    if len(actual_args) != len(declared_params):
        error = {
            "type": "error",
            "message": f"Function '{func_name}' expects {len(declared_params)} arguments, got {len(actual_args)}",
            "line": line,
            "column": column
        }
        symbol_table.setdefault("errors", []).append(error)
    
    # 递归遍历所有实际参数节点
    for arg_node in actual_args:
        _traverse_node(arg_node, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this semantic analysis function