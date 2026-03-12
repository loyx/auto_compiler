# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this validation logic

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
def _handle_return_statement(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 return_statement 类型的 AST 节点，验证返回类型与函数声明是否匹配。
    
    副作用：可能在 symbol_table["errors"] 中记录错误。
    """
    # 1. 获取当前函数名
    current_function = symbol_table.get("current_function", "")
    
    # 2. 如果当前不在函数内，记录错误
    if not current_function:
        error = {
            "type": "semantic_error",
            "message": "return outside function",
            "line": node.get("line", 0),
            "column": node.get("column", 0)
        }
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append(error)
        return
    
    # 3. 从 symbol_table 获取当前函数的返回类型
    functions = symbol_table.get("functions", {})
    func_info = functions.get(current_function, {})
    declared_return_type = func_info.get("return_type", "")
    
    # 4. 从 node 提取返回表达式的类型
    # return_statement 节点可能包含一个表达式子节点
    return_type = node.get("data_type", "")
    
    # 如果没有直接 data_type，尝试从 children 中获取表达式类型
    if not return_type:
        children = node.get("children", [])
        if children and len(children) > 0:
            # 第一个子节点通常是返回表达式
            expr_node = children[0]
            return_type = expr_node.get("data_type", "")
    
    # 5. 比较返回表达式类型与函数声明的返回类型
    # 6. 如果类型不匹配，记录类型错误
    if declared_return_type and return_type and declared_return_type != return_type:
        error = {
            "type": "type_mismatch",
            "message": f"return type '{return_type}' does not match function return type '{declared_return_type}'",
            "line": node.get("line", 0),
            "column": node.get("column", 0)
        }
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append(error)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function