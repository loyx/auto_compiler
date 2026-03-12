# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

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
#   "errors": list
# }

ErrorRecord = Dict[str, Any]
# ErrorRecord possible fields:
# {
#   "type": str,
#   "message": str,
#   "line": int,
#   "column": int,
#   "node_type": str
# }

# === main function ===
def _handle_for(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 for 循环节点。
    
    处理逻辑：
    1. 验证 children 数量为 3（迭代变量、可迭代对象、循环体）
    2. 解析并注册迭代变量到符号表
    3. 遍历可迭代对象表达式
    4. 遍历循环体 block
    
    副作用：可能修改 symbol_table（注册变量、记录错误）
    异常：不抛出，错误记录到 symbol_table['errors']
    """
    try:
        children = node.get("children", [])
        
        # 1. 验证 children 数量
        if len(children) != 3:
            error: ErrorRecord = {
                "type": "invalid_for_structure",
                "message": "For loop node must have exactly 3 children: iterator, iterable, and body",
                "line": node.get("line"),
                "column": node.get("column"),
                "node_type": "for"
            }
            symbol_table.setdefault("errors", []).append(error)
            return
        
        iterator_node = children[0]
        iterable_node = children[1]
        body_node = children[2]
        
        # 2. 处理迭代变量 - 必须是 identifier
        if iterator_node.get("type") != "identifier":
            error = {
                "type": "invalid_iterator",
                "message": f"For loop iterator must be an identifier, got {iterator_node.get('type', 'N/A')}",
                "line": iterator_node.get("line"),
                "column": iterator_node.get("column"),
                "node_type": "for"
            }
            symbol_table.setdefault("errors", []).append(error)
            return
        
        iterator_name = iterator_node.get("value")
        
        # 3. 注册迭代变量到符号表
        var_info = {
            "name": iterator_name,
            "data_type": "any",
            "scope_id": symbol_table.get("current_scope", 0),
            "line": iterator_node.get("line"),
            "column": iterator_node.get("column")
        }
        symbol_table.setdefault("variables", {})[iterator_name] = var_info
        
        # 4. 遍历可迭代对象和循环体
        _traverse_node(iterable_node, symbol_table)
        _traverse_node(body_node, symbol_table)
        
    except Exception as e:
        error = {
            "type": "for_handling_error",
            "message": str(e),
            "line": node.get("line"),
            "column": node.get("column"),
            "node_type": "for"
        }
        symbol_table.setdefault("errors", []).append(error)

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed for this function node