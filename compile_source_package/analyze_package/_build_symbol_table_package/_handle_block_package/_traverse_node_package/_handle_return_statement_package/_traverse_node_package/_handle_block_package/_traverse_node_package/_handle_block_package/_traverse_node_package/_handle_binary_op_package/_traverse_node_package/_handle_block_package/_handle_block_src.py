# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "binary_op", etc.)
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
def _handle_block(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 block 类型节点。
    
    block 代表一个作用域块（如函数体、if/while 分支等）。
    进入 block 时增加作用域层级，遍历所有子节点，离开时恢复作用域。
    """
    # 验证 children 字段
    children = node.get("children", [])
    if not isinstance(children, list):
        error_msg = f"Block node 'children' must be a list, got {type(children)}"
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append({
            "message": error_msg,
            "line": node.get("line"),
            "column": node.get("column")
        })
        return
    
    # 进入 block：保存当前作用域层级并增加
    if "scope_stack" not in symbol_table:
        symbol_table["scope_stack"] = []
    if "current_scope" not in symbol_table:
        symbol_table["current_scope"] = 0
    
    # 压栈当前 scope
    symbol_table["scope_stack"].append(symbol_table["current_scope"])
    # 增加作用域层级
    symbol_table["current_scope"] += 1
    
    # 遍历所有子节点
    for child in children:
        _traverse_node(child, symbol_table)
    
    # 离开 block：恢复作用域层级
    if symbol_table["scope_stack"]:
        symbol_table["current_scope"] = symbol_table["scope_stack"].pop()

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this internal function node
