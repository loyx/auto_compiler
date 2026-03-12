# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
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
def _handle_while(node: AST, symbol_table: SymbolTable) -> None:
    """处理 while 循环节点，管理作用域并递归遍历条件和循环体。"""
    # 1. 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 2. 获取节点位置信息
    line = node.get("line", "?")
    column = node.get("column", "?")
    
    # 3. 验证 children 结构
    children = node.get("children", [])
    if len(children) < 2:
        symbol_table["errors"].append({
            "error_type": "while_missing_condition",
            "message": "While loop must have condition and body",
            "line": line,
            "column": column
        })
        return
    
    # 4. 验证循环体是否为 block 类型
    body_node = children[1]
    if body_node.get("type") != "block":
        symbol_table["errors"].append({
            "error_type": "while_body_not_block",
            "message": "While loop body must be a block",
            "line": line,
            "column": column
        })
        return
    
    # 5. 进入新作用域
    if "scope_stack" not in symbol_table:
        symbol_table["scope_stack"] = []
    if "current_scope" not in symbol_table:
        symbol_table["current_scope"] = 0
    
    old_scope = symbol_table["current_scope"]
    symbol_table["scope_stack"].append(old_scope)
    symbol_table["current_scope"] = old_scope + 1
    
    # 6. 处理条件表达式
    condition_node = children[0]
    _traverse_node(condition_node, symbol_table)
    
    # 7. 处理循环体
    _traverse_node(body_node, symbol_table)
    
    # 8. 退出作用域
    symbol_table["current_scope"] = symbol_table["scope_stack"].pop()

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a helper function in a module