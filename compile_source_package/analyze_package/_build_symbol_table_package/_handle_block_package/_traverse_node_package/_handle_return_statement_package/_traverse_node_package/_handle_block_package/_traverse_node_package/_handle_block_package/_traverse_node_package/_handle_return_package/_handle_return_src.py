# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed - traversal is handled by parent node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "return", etc.)
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
#   "current_function": str,       # 当前函数名 (可选，可能为 None)
#   "errors": list                 # 错误列表 (可选)
# }


# === main function ===
def _handle_return(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 return 返回语句节点。
    
    验证 return 是否在函数内部，并可选检查返回类型与函数声明是否一致。
    所有错误记录到 symbol_table["errors"]，不抛出异常。
    """
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    line = node.get("line", -1)
    column = node.get("column", -1)
    
    # 1. 检查是否在函数内部
    current_function = symbol_table.get("current_function")
    if current_function is None:
        symbol_table["errors"].append({
            "type": "error",
            "message": "Return statement outside function",
            "line": line,
            "column": column
        })
        return
    
    # 2. 可选：验证返回值类型与函数声明的 return_type 是否一致
    functions = symbol_table.get("functions", {})
    if current_function in functions:
        func_info = functions[current_function]
        declared_return_type = func_info.get("return_type")
        node_return_type = node.get("data_type")
        
        # 仅当两者都存在时进行比较
        if declared_return_type is not None and node_return_type is not None:
            if declared_return_type != node_return_type:
                symbol_table["errors"].append({
                    "type": "error",
                    "message": f"Return type mismatch: expected '{declared_return_type}', got '{node_return_type}'",
                    "line": line,
                    "column": column
                })
    
    # 3. 注意：不遍历 node["children"] 中的表达式
    # 表达式遍历由父节点 traverse 函数负责，避免 child->parent 循环依赖


# === helper functions ===
# No helper functions needed for this simple validation logic

# === OOP compatibility layer ===
# Not needed - this is a semantic analysis helper function, not a framework entry point
