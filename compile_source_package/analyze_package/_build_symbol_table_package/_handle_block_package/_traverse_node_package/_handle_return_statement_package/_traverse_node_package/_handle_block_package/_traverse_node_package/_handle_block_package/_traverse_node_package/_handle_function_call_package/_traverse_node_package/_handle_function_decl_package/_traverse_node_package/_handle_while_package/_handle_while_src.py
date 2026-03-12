# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions - _traverse_node is parent function, use lazy import

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
#   "condition": Dict,       # while/if 节点的条件表达式 (单个 AST 节点)
#   "body": Dict             # while/if/func 节点的主体 (单个 AST 节点)
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list,           # 作用域栈 (存储旧 scope 值)
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 [{error_type, message, line, column}]
# }


# === main function ===
def _handle_while(node: AST, symbol_table: SymbolTable) -> None:
    """处理 while 循环语句节点。
    
    遍历条件表达式和循环体，缺失字段时记录错误到 symbol_table["errors"]。
    作用域处理由 _traverse_node 负责（当 body 是 block 类型时）。
    """
    # 延迟导入父函数，避免循环依赖
    from .._traverse_node_src import _traverse_node
    
    # 检查 condition 字段
    condition = node.get("condition")
    if condition is None:
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append({
            "error_type": "missing_condition",
            "message": "while 语句缺少条件表达式",
            "line": node.get("line", -1),
            "column": node.get("column", -1)
        })
    else:
        # 遍历条件表达式
        _traverse_node(condition, symbol_table)
    
    # 检查 body 字段
    body = node.get("body")
    if body is None:
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append({
            "error_type": "missing_body",
            "message": "while 语句缺少循环体",
            "line": node.get("line", -1),
            "column": node.get("column", -1)
        })
    else:
        # 遍历循环体
        _traverse_node(body, symbol_table)


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a plain function node