# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
# No direct child functions; _verify_children is imported at runtime via lazy import

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表（AST 节点列表）
#   "line": int,             # 行号
#   "column": int,           # 列号
#   "name": str,             # variable_ref/function_call/function_def
#   "args": list,            # function_call 参数列表
#   "params": list,          # function_def 参数列表
#   "body": AST,             # function_def 函数体
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # 变量定义表
#   "functions": Dict[str, Dict],  # 函数定义表
#   "current_scope": int,          # 当前作用域层级
# }

ContextStack = List[Dict[str, Any]]
# ContextStack possible fields:
# [
#   {"type": "function", "name": str, "return_type": str},
#   {"type": "loop", "stmt_type": "while"|"for"}
# ]


# === main function ===
def _verify_node(node: AST, symbol_table: SymbolTable, context_stack: ContextStack, filename: str) -> None:
    """验证单个 AST 节点的语义正确性。
    
    验证包括：变量引用、函数调用、控制流语句。发现错误时抛出 ValueError。
    """
    node_type = node.get("type", "")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 1. 变量引用验证
    if node_type == "variable_ref":
        name = node.get("name", "")
        variables = symbol_table.get("variables", {})
        if name not in variables:
            raise ValueError(f"{filename}:{line}:{column}: undefined variable '{name}'")
    
    # 2. 函数调用验证
    elif node_type == "function_call":
        name = node.get("name", "")
        functions = symbol_table.get("functions", {})
        
        if name not in functions:
            raise ValueError(f"{filename}:{line}:{column}: undefined function '{name}'")
        
        # 只有当 args 字段存在时才进行参数数量检查
        if "args" in node:
            args = node.get("args", [])
            func_info = functions[name]
            expected_count = func_info.get("params_count", 0)
            actual_count = len(args)
            if expected_count != actual_count:
                raise ValueError(
                    f"{filename}:{line}:{column}: function '{name}' expects {expected_count} args, got {actual_count}"
                )
    
    # 3. 控制流验证
    elif node_type == "break":
        if not _has_context_type(context_stack, "loop"):
            raise ValueError(f"{filename}:{line}:{column}: 'break' outside loop")
    
    elif node_type == "continue":
        if not _has_context_type(context_stack, "loop"):
            raise ValueError(f"{filename}:{line}:{column}: 'continue' outside loop")
    
    elif node_type == "return":
        if not _has_context_type(context_stack, "function"):
            raise ValueError(f"{filename}:{line}:{column}: 'return' outside function")
    
    # 4. 递归验证子节点（针对 block 和 function_def）
    elif node_type == "block":
        children = node.get("children", [])
        for child in children:
            _verify_child_node(child, symbol_table, context_stack, filename)
    
    elif node_type == "function_def":
        # 验证函数体（body），压入 function 上下文
        body = node.get("body")
        if body is not None:
            func_name = node.get("name", "")
            return_type = "any"  # 默认返回类型
            # 从 symbol_table 中获取实际返回类型（如果函数已定义）
            functions = symbol_table.get("functions", {})
            if func_name in functions:
                return_type = functions[func_name].get("return_type", "any")
            
            # 压入 function 上下文
            new_context = context_stack + [{"type": "function", "name": func_name, "return_type": return_type}]
            _verify_child_node(body, symbol_table, new_context, filename)
    
    # 其他类型（literal, binary_op, unary_op 等）无需语义验证，直接跳过
    # 未知类型也跳过，不报错


# === helper functions ===
def _has_context_type(context_stack: ContextStack, ctx_type: str) -> bool:
    """检查 context_stack 中是否存在指定类型的上下文条目。"""
    for entry in context_stack:
        if entry.get("type") == ctx_type:
            return True
    return False


def _verify_child_node(child_node: AST, symbol_table: SymbolTable, context_stack: ContextStack, filename: str) -> None:
    """延迟导入 _verify_children_src 并调用 _verify_children 验证子节点。"""
    from .. import _verify_children_src
    _verify_children_src._verify_children(child_node, symbol_table, context_stack, filename)


# === OOP compatibility layer ===
# No OOP wrapper needed for this semantic verification function
