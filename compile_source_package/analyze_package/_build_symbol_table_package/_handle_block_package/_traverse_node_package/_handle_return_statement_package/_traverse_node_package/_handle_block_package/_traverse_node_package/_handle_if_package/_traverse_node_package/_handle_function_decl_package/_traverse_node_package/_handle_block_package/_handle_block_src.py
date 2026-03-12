# === std / third-party imports ===
from typing import Any, Dict, Callable, Optional

# === sub function imports ===
# No child functions to import

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", "function_decl", "param_list", "param", etc.)
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
def _handle_block(node: AST, symbol_table: SymbolTable, traverse_fn: Optional[Callable[[AST, SymbolTable], None]] = None) -> None:
    """
    处理 block 节点：进入新作用域，递归遍历所有子节点，退出作用域。
    
    参数：
    - node: block 类型的 AST 节点，包含 "type"="block" 和 "children" 字段
    - symbol_table: 符号表，用于记录变量/函数信息和收集错误
    - traverse_fn: 可选的遍历函数回调（由 _traverse_node 传入自身引用）
    
    副作用：
    - 修改 symbol_table["current_scope"] 和 symbol_table["scope_stack"]
    - 通过 traverse_fn 递归处理子节点
    """
    # 1. 初始化作用域管理字段（如果不存在）
    if "scope_stack" not in symbol_table:
        symbol_table["scope_stack"] = []
    if "current_scope" not in symbol_table:
        symbol_table["current_scope"] = 0
    
    # 2. 进入新作用域：保存当前 scope 到栈，scope + 1
    symbol_table["scope_stack"].append(symbol_table["current_scope"])
    symbol_table["current_scope"] += 1
    
    # 3. 递归处理所有子节点
    if traverse_fn is not None:
        for child_node in node.get("children", []):
            traverse_fn(child_node, symbol_table)
    
    # 4. 退出作用域：恢复旧 scope
    if symbol_table["scope_stack"]:
        symbol_table["current_scope"] = symbol_table["scope_stack"].pop()

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this handler function
