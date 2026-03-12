# === std / third-party imports ===
from typing import Any, Dict, Optional, Callable

# === sub function imports ===
# No child functions to import - traverse_fn is passed as callback parameter

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
def _handle_if(
    node: AST,
    symbol_table: SymbolTable,
    traverse_fn: Optional[Callable[[AST, SymbolTable], None]] = None
) -> None:
    """
    处理 if 条件语句节点：遍历条件表达式和分支块。
    
    参数：
    - node: if 类型的 AST 节点，包含 condition、then_block、可选 else_block
    - symbol_table: 符号表（会被修改，可能记录错误）
    - traverse_fn: 回调函数，用于递归遍历子节点（由 _traverse_node 传入）
    
    副作用：
    - 递归调用 traverse_fn 处理 condition、then_block、else_block
    - 可能在 symbol_table["errors"] 中记录错误
    
    注意：
    - if 节点本身不创建新作用域（作用域由内部的 block 节点管理）
    - if 节点的 children 结构：[condition_expr, then_block, else_block?]
    """
    # 验证 traverse_fn 是否提供
    if traverse_fn is None:
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append({
            "type": "error",
            "message": "traverse_fn is required for recursive traversal",
            "line": node.get("line", "?"),
            "column": node.get("column", "?")
        })
        return
    
    # 获取子节点列表
    children = node.get("children", [])
    
    # 验证子节点数量（至少需要 condition 和 then_block）
    if len(children) < 2:
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append({
            "type": "error",
            "message": "if node must have at least 2 children (condition and then-block)",
            "line": node.get("line", "?"),
            "column": node.get("column", "?")
        })
        return
    
    # 递归遍历所有子节点：
    # children[0] = condition expression
    # children[1] = then block
    # children[2] = else block (optional)
    for child in children:
        traverse_fn(child, symbol_table)

# === helper functions ===
# No helper functions needed for this simple traversal logic

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a helper function node, not a framework entry point
