# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Note: _traverse_node is imported at function call time to avoid circular import

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
def _handle_function_call(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 function_call 类型节点。
    验证函数是否已声明，处理参数表达式。
    """
    # 确保 symbol_table 有必要的字段
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 提取函数名
    func_name = node.get("value", "")
    line = node.get("line", -1)
    column = node.get("column", -1)
    
    # 检查函数是否已声明
    functions = symbol_table.get("functions", {})
    if func_name not in functions:
        # 记录未声明函数错误
        error = {
            "type": "error",
            "message": f"Function '{func_name}' called but not declared",
            "line": line,
            "column": column
        }
        symbol_table["errors"].append(error)
    else:
        # 函数已声明，可选验证参数数量和类型
        func_decl = functions[func_name]
        expected_params = func_decl.get("params", [])
        actual_params = node.get("children", [])
        
        # 简单参数数量检查（可选）
        if len(actual_params) != len(expected_params):
            error = {
                "type": "error",
                "message": f"Function '{func_name}' expects {len(expected_params)} args, got {len(actual_params)}",
                "line": line,
                "column": column
            }
            symbol_table["errors"].append(error)
    
    # 遍历参数表达式，递归处理
    # Import _traverse_node here to avoid circular import
    # This allows tests to patch the import target correctly
    from ._traverse_node_package._traverse_node_src import _traverse_node
    for param_node in node.get("children", []):
        _traverse_node(param_node, symbol_table)

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
