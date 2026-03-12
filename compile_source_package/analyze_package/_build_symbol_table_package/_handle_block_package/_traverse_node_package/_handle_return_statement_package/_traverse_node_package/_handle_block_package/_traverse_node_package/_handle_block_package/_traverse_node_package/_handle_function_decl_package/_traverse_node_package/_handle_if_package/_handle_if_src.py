# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# _traverse_node is declared as delegated interface, import from child module
from ._traverse_node_package._traverse_node_src import _traverse_node

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
    """
    处理 if 语句节点。
    
    输入：if 类型的 AST 节点和符号表。
    处理：进入新作用域，递归处理条件表达式和语句块。
    副作用：修改 symbol_table['current_scope'] 和作用域栈。
    异常：错误记录到 symbol_table['errors']。
    """
    # 1. Push scope: save current scope and enter new scope
    old_scope = symbol_table.get("current_scope", 0)
    symbol_table.setdefault("scope_stack", []).append(old_scope)
    symbol_table["current_scope"] = old_scope + 1
    
    # 2. Check children existence
    children = node.get("children", [])
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    if not children or len(children) < 2:
        symbol_table.setdefault("errors", []).append({
            "message": "if 语句缺少子节点",
            "line": line,
            "column": column,
            "node_type": "if"
        })
    
    # 3. Recursively traverse children
    # children[0]: condition_expr (expression type)
    # children[1]: then_block (block type)
    # children[2] (optional): else_block (block type)
    for i, child in enumerate(children):
        if i < 2 or (i == 2 and len(children) > 2):
            _traverse_node(child, symbol_table)
    
    # 4. Pop scope: restore previous scope
    if symbol_table.get("scope_stack"):
        symbol_table["current_scope"] = symbol_table["scope_stack"].pop()


# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed: this is a helper function node, not a framework entry point
