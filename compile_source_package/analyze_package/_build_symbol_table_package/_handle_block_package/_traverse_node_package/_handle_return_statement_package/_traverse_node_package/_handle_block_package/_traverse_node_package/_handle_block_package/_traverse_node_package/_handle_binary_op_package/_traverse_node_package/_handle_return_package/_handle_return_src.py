# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "binary_op", "return", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (如操作符、变量名、字面量值等)
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
def _handle_return(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 return 语句节点。
    检查是否在函数内，验证返回类型兼容性。
    """
    # 1. 检查是否在函数内
    current_function = symbol_table.get("current_function")
    if not current_function:
        # 不在函数内，记录错误
        error = {
            "type": "error",
            "message": "return statement outside of function",
            "line": node.get("line", -1),
            "column": node.get("column", -1)
        }
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append(error)
        return
    
    # 2. 获取当前函数的返回类型声明
    functions = symbol_table.get("functions", {})
    func_info = functions.get(current_function, {})
    declared_return_type = func_info.get("return_type")
    
    # 3. 如果 node 有返回值表达式，遍历并验证类型
    has_return_value = "children" in node or "value" in node
    
    if has_return_value:
        # 遍历返回值表达式
        if "children" in node and node["children"]:
            for child in node["children"]:
                _traverse_node(child, symbol_table)
        
        # 4. 验证返回类型兼容性
        if declared_return_type:
            actual_type = node.get("data_type")
            if actual_type and actual_type != declared_return_type:
                # 类型不兼容，记录错误
                error = {
                    "type": "error",
                    "message": f"return type mismatch: expected {declared_return_type}, got {actual_type}",
                    "line": node.get("line", -1),
                    "column": node.get("column", -1)
                }
                if "errors" not in symbol_table:
                    symbol_table["errors"] = []
                symbol_table["errors"].append(error)
    else:
        # 没有返回值，检查函数是否声明为 void 或无返回类型
        if declared_return_type and declared_return_type not in ("void", None, ""):
            error = {
                "type": "error",
                "message": f"function expects return value of type {declared_return_type}, but return has no value",
                "line": node.get("line", -1),
                "column": node.get("column", -1)
            }
            if "errors" not in symbol_table:
                symbol_table["errors"] = []
            symbol_table["errors"].append(error)


# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
