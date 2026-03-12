# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No external sub function imports needed; _dispatch_node is declared inline

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char" 或 "bool")
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
    处理 if 语句节点：验证条件表达式类型，管理作用域，递归处理子节点。
    
    副作用：
    - 通过 _dispatch_node 递归处理子节点，可能修改 symbol_table
    - 条件类型不匹配时记录错误到 symbol_table["errors"]
    - 管理 current_scope 和 scope_stack
    """
    
    def _dispatch_node(n: AST, st: SymbolTable) -> None:
        """
        节点分发器：根据节点类型调用相应的 handler。
        内部声明以避免与 _traverse_node 的循环依赖。
        """
        node_type = n.get("type", "")
        
        # 根据节点类型分发到对应 handler
        # 注意：实际 handler 由子函数节点提供，此处为简化声明
        # 真实实现中应 import 并调用具体 handler
        if node_type == "if":
            from ._handle_if_package._handle_if_src import _handle_if as handler
            handler(n, st)
        elif node_type == "block":
            from ._handle_block_package._handle_block_src import _handle_block as handler
            handler(n, st)
        elif node_type == "binary_op":
            from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op as handler
            handler(n, st)
        elif node_type == "identifier":
            from ._handle_identifier_package._handle_identifier_src import _handle_identifier as handler
            handler(n, st)
        elif node_type == "assignment":
            from ._handle_assignment_package._handle_assignment_src import _handle_assignment as handler
            handler(n, st)
        elif node_type == "var_decl":
            from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl as handler
            handler(n, st)
        elif node_type == "while":
            from ._handle_while_package._handle_while_src import _handle_while as handler
            handler(n, st)
        elif node_type == "literal":
            # literal 节点通常无需特殊处理
            pass
        else:
            # 未知节点类型，记录警告或跳过
            pass
    
    children = node.get("children", [])
    
    # 检查子节点数量
    if len(children) < 2:
        symbol_table.setdefault("errors", []).append({
            "type": "invalid_if_structure",
            "message": f"if 节点缺少必要条件或语句块：期望至少 2 个子节点，实际为 {len(children)}",
            "line": node.get("line", "?"),
            "column": node.get("column", "?")
        })
        return
    
    # 1. 处理条件表达式 (children[0])
    condition = children[0]
    _dispatch_node(condition, symbol_table)
    
    # 2. 验证条件表达式类型
    cond_type = condition.get("data_type", "")
    if cond_type and cond_type not in ("bool", "int"):
        symbol_table.setdefault("errors", []).append({
            "type": "invalid_condition_type",
            "message": f"if 条件表达式类型错误：期望 bool 或 int，实际为 {cond_type}",
            "line": node.get("line", "?"),
            "column": node.get("column", "?")
        })
    
    # 3. 进入 if 体作用域
    old_scope = symbol_table.get("current_scope", 0)
    symbol_table.setdefault("scope_stack", []).append(old_scope)
    symbol_table["current_scope"] = old_scope + 1
    
    # 4. 处理 if 体 (children[1])
    _dispatch_node(children[1], symbol_table)
    
    # 5. 退出 if 体作用域
    scope_stack = symbol_table.get("scope_stack", [])
    if scope_stack:
        symbol_table["current_scope"] = scope_stack.pop()
    
    # 6. 处理 else 体 (children[2]，如果存在)
    # else 体与 if 体共享同一作用域层级，无需再次修改 current_scope
    if len(children) > 2:
        _dispatch_node(children[2], symbol_table)


# === helper functions ===
# No external helper functions needed

# === OOP compatibility layer ===
# Not required for this function node
