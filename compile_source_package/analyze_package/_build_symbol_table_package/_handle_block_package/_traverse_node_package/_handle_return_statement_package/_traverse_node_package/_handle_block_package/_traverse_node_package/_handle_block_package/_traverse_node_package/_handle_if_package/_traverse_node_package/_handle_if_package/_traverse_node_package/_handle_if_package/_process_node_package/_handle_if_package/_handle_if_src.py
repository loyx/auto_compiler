# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._process_node_package._process_node_src import _process_node
from ._process_block_package._process_block_src import _process_block
from ._push_scope_package._push_scope_src import _push_scope
from ._pop_scope_package._pop_scope_src import _pop_scope

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "data_type": str,
#   "line": int,
#   "column": int,
#   "condition": AST,
#   "then_branch": AST,
#   "else_branch": AST
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_if(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 if 语句节点。
    
    处理逻辑：
    1. 从 node 中提取 condition、then_branch、else_branch
    2. 创建新的作用域（if 语句块的作用域）
    3. 处理条件表达式
    4. 处理 then 分支语句块
    5. 如果存在 else_branch，处理 else 分支语句块
    6. 退出 if 语句作用域
    7. 所有错误记录到 symbol_table["errors"]，不抛出异常
    """
    try:
        # 提取 if 语句各组成部分
        condition = node.get("condition")
        then_branch = node.get("then_branch")
        else_branch = node.get("else_branch")
        
        # 验证必需字段
        if condition is None:
            error_msg = f"if 语句缺少 condition 字段 (line {node.get('line', 'unknown')})"
            symbol_table.setdefault("errors", []).append(error_msg)
            return
        
        if then_branch is None:
            error_msg = f"if 语句缺少 then_branch 字段 (line {node.get('line', 'unknown')})"
            symbol_table.setdefault("errors", []).append(error_msg)
            return
        
        # 创建 if 语句作用域
        _push_scope(symbol_table)
        
        # 处理条件表达式
        if condition is not None:
            _process_node(condition, symbol_table)
        
        # 处理 then 分支
        if then_branch is not None:
            _process_block(then_branch, symbol_table)
        
        # 处理 else 分支（如果存在）
        if else_branch is not None:
            _process_block(else_branch, symbol_table)
        
        # 退出 if 语句作用域
        _pop_scope(symbol_table)
        
    except Exception as e:
        # 捕获所有异常，记录到 errors，不抛出
        error_msg = f"处理 if 语句时发生错误：{str(e)} (line {node.get('line', 'unknown')})"
        symbol_table.setdefault("errors", []).append(error_msg)

# === helper functions ===
# No helper functions needed - all logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed for this function node