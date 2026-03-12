# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions to import

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_decl", "return", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (对于 return 节点，可能是返回值表达式)
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
#   "current_function": str,       # 当前函数名 (可选，None 表示不在函数内)
#   "errors": list                 # 错误列表 (存储错误信息字典)
# }

ErrorDict = Dict[str, Any]
# ErrorDict possible fields:
# {
#   "line": int,
#   "column": int,
#   "message": str,
#   "error_type": str  # 如 "return_outside_function", "type_mismatch", "missing_return_value"
# }


# === main function ===
def _handle_return(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 return 返回语句节点。
    
    验证 return 语句是否在函数内使用，以及返回值类型是否与函数声明匹配。
    副作用：可能添加错误字典到 symbol_table["errors"]。
    """
    # 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 步骤 1: 获取当前函数名
    current_function = symbol_table.get("current_function")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 步骤 2: 检查是否在函数内
    if current_function is None:
        error_dict: ErrorDict = {
            "line": line,
            "column": column,
            "message": "'return' statement used outside of function",
            "error_type": "return_outside_function"
        }
        symbol_table["errors"].append(error_dict)
        return
    
    # 步骤 3: 获取函数声明的返回类型
    functions = symbol_table.get("functions", {})
    func_decl = functions.get(current_function)
    
    if func_decl is None:
        # 函数未声明（理论上不应发生，但做防御性处理）
        error_dict = {
            "line": line,
            "column": column,
            "message": f"current function '{current_function}' not found in symbol table",
            "error_type": "function_not_found"
        }
        symbol_table["errors"].append(error_dict)
        return
    
    declared_return_type = func_decl.get("return_type")
    
    # 步骤 4: 检查返回值类型是否匹配
    return_value = node.get("value")
    
    if return_value is not None:
        # return 有返回值，需要检查类型
        if isinstance(return_value, dict) and "data_type" in return_value:
            actual_return_type = return_value.get("data_type")
            
            if declared_return_type is not None and actual_return_type != declared_return_type:
                error_dict = {
                    "line": line,
                    "column": column,
                    "message": f"return type mismatch, expected '{declared_return_type}' but got '{actual_return_type}'",
                    "error_type": "type_mismatch"
                }
                symbol_table["errors"].append(error_dict)
        
        # 步骤 6: 递归处理返回值表达式中的子节点
        if isinstance(return_value, dict):
            _process_expression_node(return_value, symbol_table)
    else:
        # return 没有返回值，检查函数是否声明为 void 或无返回类型
        if declared_return_type is not None and declared_return_type != "void":
            # 函数声明了返回类型但 return 没有返回值
            error_dict = {
                "line": line,
                "column": column,
                "message": f"function '{current_function}' expects return type '{declared_return_type}' but no value returned",
                "error_type": "missing_return_value"
            }
            symbol_table["errors"].append(error_dict)


# === helper functions ===
def _process_expression_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    递归处理表达式节点中的子节点。
    
    遍历 AST 节点的 children 列表，对每个子节点进行必要的语义检查。
    当前实现为占位，可根据需要扩展具体检查逻辑。
    """
    children = node.get("children", [])
    for child in children:
        if isinstance(child, dict):
            # 可以在此处根据 child["type"] 调用不同的处理函数
            # 目前仅递归遍历
            _process_expression_node(child, symbol_table)


# === OOP compatibility layer ===
# Not needed for this helper function node
