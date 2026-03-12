# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# only import child functions
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
# define the data structures used between parent and child functions
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
def _handle_if(node: AST, symbol_table: SymbolTable) -> None:
    """处理 if 语句节点。
    
    处理逻辑：
    1. 验证条件表达式类型（应为 int 类型）
    2. 进入新作用域处理 then 分支
    3. 如果存在 else 分支，进入新作用域处理 else 分支
    4. 错误记录到 symbol_table["errors"]
    
    Args:
        node: AST - if 类型的 AST 节点，包含 "type"="if"，"children" 包含条件表达式、then 分支、else 分支（可选）
        symbol_table: SymbolTable - 符号表，用于记录变量、作用域信息和收集错误
    
    Returns:
        None: 函数通过修改 symbol_table 产生副作用
    """
    # 1. 验证条件表达式类型
    condition = node["children"][0]
    if condition.get("data_type") != "int":
        symbol_table.setdefault("errors", []).append({
            "type": "type_error",
            "message": "if 条件表达式必须为 int 类型",
            "line": condition.get("line", 0),
            "column": condition.get("column", 0)
        })
    
    # 2. 处理 then 分支（第二个子节点）
    # 进入新作用域
    symbol_table.setdefault("scope_stack", []).append(symbol_table.get("current_scope", 0))
    symbol_table["current_scope"] = symbol_table.get("current_scope", 0) + 1
    
    then_branch = node["children"][1]
    _traverse_node(then_branch, symbol_table)
    
    # 退出 then 分支作用域
    symbol_table["current_scope"] = symbol_table["scope_stack"].pop()
    
    # 3. 处理 else 分支（第三个子节点，可选）
    if len(node["children"]) > 2:
        # 进入新作用域（else 分支独立作用域）
        symbol_table["scope_stack"].append(symbol_table.get("current_scope", 0))
        symbol_table["current_scope"] = symbol_table.get("current_scope", 0) + 1
        
        else_branch = node["children"][2]
        _traverse_node(else_branch, symbol_table)
        
        # 退出 else 分支作用域
        symbol_table["current_scope"] = symbol_table["scope_stack"].pop()

# === helper functions ===
# 当前函数逻辑清晰，无需额外 helper 函数

# === OOP compatibility layer ===
# 当前函数为 AST 遍历工具函数，无需 OOP wrapper
# 省略该 section