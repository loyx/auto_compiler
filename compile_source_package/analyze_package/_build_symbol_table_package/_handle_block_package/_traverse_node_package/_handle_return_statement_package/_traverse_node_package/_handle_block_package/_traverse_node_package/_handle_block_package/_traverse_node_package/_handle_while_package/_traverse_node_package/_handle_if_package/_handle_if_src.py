# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Note: _traverse_node is imported inside the function to avoid circular dependency

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
def _handle_if(node: AST, symbol_table: SymbolTable) -> None:
    """处理 if 条件分支节点，验证条件和分支体中的变量使用。"""
    # Lazy import to avoid circular dependency
    from ._traverse_node_package._traverse_node_src import _traverse_node
    
    children = node.get("children", [])
    
    # 验证 if 节点结构完整性
    if len(children) < 2:
        _record_error(
            symbol_table,
            "invalid_syntax",
            "if node must have at least condition and then_branch",
            node.get("line", 0),
            node.get("column", 0)
        )
        return
    
    condition = children[0]
    then_branch = children[1]
    else_branch = children[2] if len(children) == 3 else None
    
    # 处理条件表达式
    _traverse_node(condition, symbol_table)
    
    # 处理 then 分支
    _traverse_node(then_branch, symbol_table)
    
    # 处理 else 分支（如果存在）
    if else_branch is not None:
        _traverse_node(else_branch, symbol_table)


# === helper functions ===
def _record_error(
    symbol_table: SymbolTable,
    error_type: str,
    message: str,
    line: int,
    column: int
) -> None:
    """记录错误到符号表的 errors 列表。"""
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    symbol_table["errors"].append({
        "type": error_type,
        "message": message,
        "line": line,
        "column": column
    })


# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
