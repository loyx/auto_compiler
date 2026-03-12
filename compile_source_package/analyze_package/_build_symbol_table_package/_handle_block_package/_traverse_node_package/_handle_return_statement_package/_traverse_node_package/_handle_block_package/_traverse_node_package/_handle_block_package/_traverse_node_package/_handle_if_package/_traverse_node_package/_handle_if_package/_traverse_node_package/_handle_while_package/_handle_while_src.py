# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions delegated

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "data_type": str,
#   "line": int,
#   "column": int
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
def _handle_while(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 while 循环节点。
    
    遍历条件表达式和循环体，管理作用域。
    不实际执行循环，只做 AST 遍历和符号表管理。
    """
    try:
        children = node.get("children", [])
        
        # 验证 children 数量
        if len(children) < 2:
            error_msg = f"while node expects 2 children (condition, body), got {len(children)}"
            symbol_table.setdefault("errors", []).append(error_msg)
            return
        
        condition_expr = children[0]
        body_block = children[1]
        
        # 进入循环体前 push 新作用域
        _push_scope(symbol_table)
        
        # 遍历条件表达式
        _traverse_ast_node(condition_expr, symbol_table)
        
        # 遍历循环体
        _traverse_ast_node(body_block, symbol_table)
        
        # 退出循环体后 pop 作用域
        _pop_scope(symbol_table)
        
    except Exception as e:
        symbol_table.setdefault("errors", []).append(f"Error handling while node: {str(e)}")


# === helper functions ===
def _push_scope(symbol_table: SymbolTable) -> None:
    """进入新作用域"""
    symbol_table.setdefault("scope_stack", [])
    symbol_table.setdefault("current_scope", 0)
    
    symbol_table["scope_stack"].append(symbol_table["current_scope"])
    symbol_table["current_scope"] += 1


def _pop_scope(symbol_table: SymbolTable) -> None:
    """退出当前作用域"""
    scope_stack = symbol_table.get("scope_stack", [])
    if scope_stack:
        symbol_table["current_scope"] = scope_stack.pop()


def _traverse_ast_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    通用 AST 节点遍历函数。
    根据节点类型分发到不同处理器，或递归遍历 children。
    """
    if not isinstance(node, dict):
        return
    
    node_type = node.get("type", "")
    children = node.get("children", [])
    
    # 递归遍历所有子节点
    for child in children:
        _traverse_ast_node(child, symbol_table)


# === OOP compatibility layer ===
# Not required for this function node
